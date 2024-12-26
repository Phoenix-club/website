from django.shortcuts import render 
from django.http import HttpResponse
from .serializers import EventSerializer,RegistrationSerializer
from rest_framework import generics
from .models import * 
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

def landing(request):
    return HttpResponse("landing.html")

 

class EventListView(generics.ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class RegistrationView(generics.CreateAPIView):
    queryset = Registration.objects.all();
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self,request,*args):
        payload=request.data
        registrant=payload['registrant']
        registrant_email=payload['registrant_email']   
        registrant_phone=payload['registrant_phone']   
        branch=payload['branch']   
        year=payload['year']   
        event=payload['event'] 
        team_name=payload['team_name']
        try:
            event = Events.objects.get(id=event)
            Registration.objects.create(registrant=registrant,registrant_email=registrant_email,registrant_phone=registrant_phone,branch=branch,year=year,event=event,team_name=team_name)
            return Response(
                {
                    "message":"Created Successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {
                    "message":"Something Went Wrong",
                }
            )