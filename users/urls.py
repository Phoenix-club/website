from django.urls import path,include
from .views import * 
urlpatterns = [
  path("",landing,name= "landing_view"),
]
