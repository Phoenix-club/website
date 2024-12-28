from django.shortcuts import render,get_object_or_404,redirect
from users.models import *
from .forms import *
from django.http import HttpResponse
import openpyxl
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Redirect to a list of events
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


def event_list(request):
    events = Events.objects.all().order_by('-date')
    return render(request, 'event_list.html', {'events': events})

def event_detail(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    registrations = Registration.objects.filter(event=event)
    registration_with_team = []
    for registration in registrations:
        if event.event_type != 'individual':
            team_members = TeamMember.objects.filter(registration=registration)
        else:
            team_members = []  
        registration_with_team.append({
            'registration': registration,
            'team_members': team_members
        })
    return render(request, "event_detail.html", {
        'event': event,
        'registration_with_team': registration_with_team
    })

def revenue_gen(request,pk):
    event = get_object_or_404(Events,pk=pk)
    if event.paid is False :
        return HttpResponse("this event is free ie not paid")

    participants = Registration.objects.filter(event =event)
    collection =0
    collection = participants.count()*event.fees
    
    return render(request, "revenue.html",{"collection":collection})

def export_event_registrations(request, event_pk):
    event = get_object_or_404(Events, pk=event_pk)

    # Create a workbook and add a sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"Registrations - {event.name}"

    # Add headers
    sheet['A1'] = 'Registrant Name'
    sheet['B1'] = 'Email'
    sheet['C1'] = 'Phone'
    sheet['D1'] = 'Team Name'
    sheet['E1'] = 'Registration Time'
    sheet['F1'] = 'Payment Screenshot'
    sheet['G1'] = 'Team Member Name'
    sheet['H1'] = 'Team Member Email'
    sheet['I1'] = 'Team Member Phone'

    # Populate the sheet with registration data
    registrations = Registration.objects.filter(event=event)
    row = 2
    for registration in registrations:
        # Write the registration data
        sheet[f'A{row}'] = registration.registrant
        sheet[f'B{row}'] = registration.registrant_email
        sheet[f'C{row}'] = registration.registrant_phone
        sheet[f'D{row}'] = registration.team_name or 'N/A'
        sheet[f'E{row}'] = registration.registration_time
        sheet[f'F{row}'] = 'Yes' if registration.payment_screenshot else 'No'

        # Write the team members data
        team_members = TeamMember.objects.filter(registration=registration)
        for member in team_members:
            sheet[f'G{row}'] = member.name
            sheet[f'H{row}'] = member.email
            sheet[f'I{row}'] = member.phone
            row += 1

        row += 1  # Skip a row between registrations

    # Return the Excel file as a response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="registrations_{event.name}.xlsx"'
    workbook.save(response)
    return response

        
