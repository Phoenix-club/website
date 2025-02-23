from django.shortcuts import render,get_object_or_404,redirect
from users.models import *
from .forms import *
from django.http import HttpResponse
import openpyxl
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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
    event = get_object_or_404(Events, pk=event_pk)
    registrations = Registration.objects.filter(event=event)
    registration_with_team = []
    
    for registration in registrations:
        team_members = TeamMember.objects.filter(registration=registration) if event.event_type != 'individual' else []
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

from django.utils.timezone import is_aware, make_naive

def export_event_registrations(request, event_pk):
    event = get_object_or_404(Events, pk=event_pk)

    # Create Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"Registrations - {event.name}"

    # Define column headers (No team members)
    headers = [
        "Registrant Name", "Email", "Phone", "Team Name", "Registration Time",
        "Payment Screenshot", "Approval"
    ]
    sheet.append(headers)

    # Fetch all registrations for the event
    registrations = Registration.objects.filter(event=event)
    
    for registration in registrations:
        # Convert timezone-aware datetime to naive datetime
        reg_time = registration.registration_time
        if is_aware(reg_time):
            reg_time = make_naive(reg_time)

        # Add registration data (No team members)
        sheet.append([
            registration.registrant,
            registration.registrant_email,
            registration.registrant_phone,
            registration.team_name or "N/A",
            reg_time.strftime('%Y-%m-%d %H:%M:%S'),
            "Yes" if registration.payment_screenshot else "No",
            "Yes" if registration.approval else "No"
        ])

    # Prepare response with the Excel file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="registrations_{event.name}.xlsx"'
    workbook.save(response)
    
    return response
@require_POST
def approve_registration(request, registration_pk):
    registration = get_object_or_404(Registration, pk=registration_pk)
    approval_status = request.POST.get("approval")

    if approval_status == "approve":
        registration.approval = True
    elif approval_status == "reject":
        registration.approval = False
    else:
        return HttpResponse("Invalid action", status=400)

    registration.save()
    return redirect('event_detail', event_pk=registration.event.pk)
       
