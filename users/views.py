from django.shortcuts import render 
from django.http import HttpResponse

def landing(request):
    return HttpResponse("landing.html")

 
