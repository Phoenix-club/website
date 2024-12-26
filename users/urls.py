from django.urls import path,include
from .views import * 
urlpatterns = [
  path("",landing,name= "landing_view"),
  path("events/",EventListView.as_view(),name='Event-list'),
  path("register/",RegistrationView.as_view(),name='event-registration'),
]
