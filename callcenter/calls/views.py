from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


@login_required
def index(request):
    calls = Call.objects.filter(call_operator=request.user).select_related('call_result').order_by('-date')[:10]
    template = 'calls/index.html'
    context = {
        'calls': calls
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
def save(request):
    date = datetime.datetime.now().isoformat()
    call_number = request.POST.get('call_number')
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
    if( request.POST.get('date_of_birth') != None): 
        date_of_birth = datetime.datetime.strptime(request.POST.get('date_of_birth'), '%d.%m.%Y').isoformat()
    if( request.POST.get('callback_number') != None):
        callback_number = request.POST.get('callback_number')
    else:
        callback_number = None
#    call_result = Call_result.objects.get(name="Обработан")
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
#        registration_covid_date=registration_covid_date,
        manipulation=manipulation,
        hospital=hospital,
        city=city,
        question=question,
        address=address,
        callback_number=callback_number,
#        call_result=call_result,
        call_operator=call_operator,
        )
    call.save()

    patient = Patient(
        patient_fio=patient_fio,
        date_of_birth=date_of_birth,
        call=call
    )
    patient.save()
    print(call.id)

    return HttpResponseRedirect("/")
