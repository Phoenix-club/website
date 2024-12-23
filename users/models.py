from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import datetime
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.db.models import F

class Events(models.Model):
    Event_Types = [
            ('individiual','Individual'),
            ('team','Team'),
            ]
    name =models.CharField(max_length=250)
    description = models.TextField(blank = True,null=True)
    date = models.DateTimeField()
    deadline = models.DateTimeField()
    venue = models.CharField(max_length = 255)
    paid = models.BooleanField(default = False)
    event_capacity= models.PositiveIntegerField()
    current_registration = models.PositiveIntegerField(default =0)    
    event_type = models.CharField(max_length =15,choices=Event_Types,default ='individiual')

    def can_register(self):
        if isinstance(self.deadline, str):
            # Convert string to datetime object
            self.deadline = datetime.strptime(self.deadline, "%Y-%m-%d %H:%M:%S")
        
        # Make sure `self.deadline` is timezone-aware
        if timezone.is_naive(self.deadline):
            self.deadline = timezone.make_aware(self.deadline, timezone.get_current_timezone())

        # Compare the `deadline` with the current time
        return self.current_registration < self.event_capacity and self.deadline > timezone.now()

    def __str__(self):
        return self.name
class Registration(models.Model):
    registrant = models.CharField(max_length=250)
    registrant_email = models.EmailField()
    registrant_phone = models.CharField(max_length=13)
    registration_time = models.DateTimeField(auto_now_add=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='registrations', db_index=True)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    

    def clean(self):
        if self.event.event_type == 'individual' and self.team_name:
            raise ValidationError("team registrations are not allowed for this event")
        if not self.event.can_register():
            raise ValidationError("Cannot register: event is full or deadline has passed.")

    def __str__(self):
        return f"{self.registrant} - {self.event.name}"


class TeamMember(models.Model):
    registration = models.ForeignKey(Registration,on_delete =models.CASCADE,related_name='team_members')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=13,null=True,blank=True)


    def clean(self):
        if self.registration.event.event_type =='individual':
            raise ValidationError("cannot add team members in individual event")

    def __str__(self):
        return  f"{self.name} ({self.email}) - Team: {self.registration.team_name or 'N/A'}"


@receiver(post_save, sender =Registration)
def increment_registration_count(sender,instance,created, **kwargs):
    if created:
        event = instance.event
        event.current_registration += 1
        event.save()
