from rest_framework import serializers
from rest_framework import generics
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id','image']

class EventSerializer(serializers.ModelSerializer):
    images= EventImageSerializer(many =True,read_only =True)
    class Meta:
        model = Events
        fields="__all__"

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model =TeamMember
        fields = ['id','name','email','phone']

import json

class RegistrationSerializer(serializers.ModelSerializer):
    team_members = TeamMemberSerializer(many=True, required=False)

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
            'payment_screenshot',
            'team_members',
        ]

    def create(self, validated_data):
        # Extract team_members JSON string if sent in form-data
        request = self.context.get('request')
        if request and isinstance(request.data.get("team_members"), str):
            try:
                team_members_data = json.loads(request.data["team_members"])
            except json.JSONDecodeError:
                raise serializers.ValidationError({"team_members": "Invalid JSON format."})
        else:
            team_members_data = validated_data.pop('team_members', [])

        # Create Registration
        registration = Registration.objects.create(**validated_data)

        # Save each team member
        for member_data in team_members_data:
            TeamMember.objects.create(registration=registration, **member_data)

        return registration

