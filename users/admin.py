from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib import admin
from .models import EventImage, Events, Registration, TeamMember

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]
    search_fields = ["image"]

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "deadline", "venue", "paid", "event_capacity", "current_registration", "event_type"]
    list_filter = ["paid", "event_type"]
    search_fields = ["name", "venue"]
    ordering = ["date"]

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["registrant", "registrant_email", "event", "registration_time", "approval"]
    list_filter = ["approval", "event"]
    search_fields = ["registrant", "registrant_email", "registrant_phone"]
    ordering = ["-registration_time"]

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "registration"]
    search_fields = ["name", "email"]
    ordering = ["name"]

