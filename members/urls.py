from django.urls import path,include
from .views import *

urlpatterns = [
    path('events/add/', add_event, name='add_event'),
    path('events/', event_list, name='event_list'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('event_revenue<int:pk>',revenue_gen,name='event_revenue'),
    path('event_excel_export',export_event_registrations,name ='excel')
]
