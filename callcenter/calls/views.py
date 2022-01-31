import email
from multiprocessing import context
from re import template
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Journal, Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required




@login_required
def index(request):
    calls = Call.objects.filter(call_operator=request.user).select_related('call_result').order_by('-date')[:10]
    template = 'calls/index.html'
    context = {
        'calls': calls,
    }
    return render(request, template, context)


@login_required
def add(request):
    template = 'calls/add.html'
    subjects = Subject.objects.all()
    sub_subjects = Sub_subject.objects.all()
    manipulations = Manipulation.objects.all()
    citys = City.objects.all()
    hospitals = Hospital.objects.all()
    call_results = Call_result.objects.all()
    context = {
        'subjects': subjects,
        'sub_subjects': sub_subjects,
        'manipulations': manipulations,
        'hospitals': hospitals,
        'citys': citys,
        'call_results': call_results

    }
    return render(request, template, context)

@login_required
def show(request, id):
    template = 'calls/show.html'
    call = Call.objects.get(pk=id)
    patient = Patient.objects.filter(call=call)
    journal = Journal.objects.filter(call=call)
    context = {
        'call': call,
        'patient': patient,
        'journal': journal,
    }
    return render(request, template, context)


@login_required
def save(request):
    date = datetime.datetime.now().isoformat()
    call_number = request.POST.get('call_number').strip()
    if( request.POST.get('subject') != None):
        subject = Subject.objects.get(id=request.POST.get('subject'))
    else:
        subject = None
    if( request.POST.get('sub_subject') != None):
        sub_subject = Sub_subject.objects.get(id=request.POST.get('sub_subject'))
    else:
        sub_subject = None
    if( request.POST.get('manipulation') != None):
        manipulation = Manipulation.objects.get(id=request.POST.get('manipulation'))
    else:
        manipulation = None
    if( request.POST.get('hospital') != None):
        hospital = Hospital.objects.get(id=request.POST.get('hospital'))
    else:
        hospital = None
    if( request.POST.get('city') != None):    
        city = City.objects.get(id=request.POST.get('city'))
    else:
        city = None
    question = request.POST.get('question')
    if( request.POST.get('street') != None):
        street = request.POST.get('street')
    else:
        street = None
    if( request.POST.get('number') != None):
        number = request.POST.get('number')
    else:
        number = None
    if( request.POST.get('building') != None):    
        building = request.POST.get('building')
    else:
        building = None
    if( request.POST.get('room') != None):
        room = request.POST.get('room')
    else:
        room = None
    if( request.POST.get('patient_fio') != None):
        patient_fio = request.POST.get('patient_fio')
    else:
        patient_fio = None
    if( request.POST.get('date_of_birth') == '' ):
        date_of_birth = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
    else:
        date_of_birth = datetime.datetime.strptime(request.POST.get('date_of_birth').strip(), '%d.%m.%Y').isoformat()
    if( request.POST.get('registration_covid_date') == ''): 
         registration_covid_date = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
    else:
         registration_covid_date = datetime.datetime.strptime(request.POST.get('registration_covid_date').strip(), '%d.%m.%Y').isoformat()    
    if( request.POST.get('callback_number') != None):
        callback_number = request.POST.get('callback_number').strip()
    else:
        callback_number = None
    if( request.POST.get('call_result') != None):
        call_result = Hospital.objects.get(id=request.POST.get('call_result'))
    else:
        call_result = None
    if(request.POST.get('complited') == 'on'):
        complited = True
    else:
        complited = False 
    if(request.POST.get('urgent') == 'on'):
        urgent = True
    else:
        urgent = False
    if (complited is True and hospital is None):
        active = False
    else:
        active = True
    
    call_operator = request.user
    address = Address(
        street=street,
        number=number,
        building=building,
        room=room
    )
    address.save()
    call = Call(
        date=date,
        call_number=call_number,
        subject=subject,
        sub_subject=sub_subject,
        registration_covid_date=registration_covid_date,
        manipulation=manipulation,
        hospital=hospital,
        city=city,
        question=question,
        address=address,
        callback_number=callback_number,
        call_result=call_result,
        call_operator=call_operator,
        complited=complited,
        urgent=urgent,
        active=active,
        )
    call.save()
    if (request.POST.get('patient_fio') != None): 
        patient = Patient(
            patient_fio=patient_fio,
            date_of_birth=date_of_birth,
            call=call
        )
        patient.save()
    

    return HttpResponseRedirect("/")

@login_required
@permission_required('calls.view_hospital')
def hospital_all(request):
    hospital = Hospital.objects.get(email=request.user.email)
    template = "hospitals/index.html"
    calls = Call.objects.filter(hospital=hospital).select_related('call_result').order_by('-date')[:10]
    context = {
        "hospital": hospital.name,
        "calls":calls
    }
    return render(request,template,context)

@login_required
@permission_required('calls.view_hospital')
def hospital_show(request,pk):
    template = 'calls/show.html'
    call = Call.objects.filter(pk=pk).select_related('hospital').select_related('subject').select_related('sub_subject').select_related('manipulation').select_related('city').select_related('address')
    context = {
        'call': call,
    }
    return render(request, template, context)