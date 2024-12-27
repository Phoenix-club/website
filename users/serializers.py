from rest_framework import serializers
from rest_framework import generics
from .models import *
from rest_framework.exceptions import ValidationError

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
    def create(self , validated_data):
        team_members_data = validated_data.pop('team_members',[])
        registration =Registration.objects.create(**validated_data)

        for member_data in team_members_data:
            TeamMember.objects.create(registration =registration,**member_data)

        return registration
    def validate(self,data):
        event =data['event']
        if event.event_type =='team'and not data.get('team_name'):
            raise serializers.ValidationError("team name is required for team registration")
        return data
