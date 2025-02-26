from django.urls import path,include
from .views import *

urlpatterns = [
    path('events/add/', add_event, name='add_event'),
    path('events/', event_list, name='event_list'),
    path('events/<int:event_pk>/', event_detail, name='event_detail'),
    path('event_revenue/<int:pk>',revenue_gen,name='event_revenue'),
    path('event_excel_export/<int:event_pk>/',export_event_registrations,name ='excel'),
    path('approve-registration/<int:registration_pk>/', approve_registration, name='approve_registration'),
    path('event/<int:event_pk>/update/', update_event, name='update_event'),

]
