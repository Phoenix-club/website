from rest_framework import serializers
from rest_framework import generics
from .models import *

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields="__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'registrant',
            'registrant_email',
            'registrant_phone',
            'branch',
            'year',
            'event',
            'team_name',
        ]