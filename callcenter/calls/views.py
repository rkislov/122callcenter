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
    subject = Subject.objects.get(id=request.POST.get('subject'))
    sub_subject = Sub_subject.objects.get(id=request.POST.get('sub_subject'))
    registration_covid_date = datetime.datetime.strptime(request.POST.get('registration_covid_date'), '%d.%m.%Y').isoformat()
    manipulation = Manipulation.objects.get(id=request.POST.get('manipulation'))
    hospital = Hospital.objects.get(id=request.POST.get('hospital'))
    city = City.objects.get(id=request.POST.get('city'))
    question = request.POST.get('question')
    street = request.POST.get('street')
    number = request.POST.get('number')
    building = request.POST.get('building')
    room = request.POST.get('room')
    patient_fio = request.POST.get('patient_fio')
    date_of_birth = datetime.datetime.strptime(request.POST.get('date_of_birth'), '%d.%m.%Y').isoformat()
    callback_number = request.POST.get('callback_number')
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
        registration_covid_date=registration_covid_date,
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
