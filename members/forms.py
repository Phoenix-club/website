from django import forms
from users.models import Events

class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = [
            'name', 
            'description', 
            'date', 
            'deadline', 
            'venue', 
            'paid', 
            'event_capacity', 
            'event_type', 
            'fees', 
            'poster', 
            'images'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add event details'}),
            'poster': forms.ClearableFileInput(),
            'images': forms.CheckboxSelectMultiple(),  
        }

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get('deadline')
        date = cleaned_data.get('date')
        event_capacity = cleaned_data.get('event_capacity')

        if deadline and date:
            if deadline >= date:
                raise forms.ValidationError("Deadline must be before the event date.")
        if event_capacity is not None and event_capacity <= 0:
            raise forms.ValidationError("Event capacity must be greater than zero.")
        return cleaned_data

