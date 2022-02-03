import email
from email import message
from multiprocessing import context
from pyexpat import model
from re import template
from unittest.mock import call
from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Journal, Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from callcenter.settings import EMAIL_HOST_USER
from django.core.mail import utils,EmailMessage
from django.db import connections
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import AddForm





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
    patients = Patient.objects.filter(call=call)
    journals = Journal.objects.filter(call=call)
    context = {
        'call': call,
        'patients': patients,
        'journals': journals,
    }
    return render(request, template, context)


@login_required
def save(request):
    date = datetime.datetime.now().isoformat()
    call_number = request.POST.get('call_number').strip()
    if (request.POST.get('subject') != None):
        subject = Subject.objects.get(id=request.POST.get('subject'))
    else:
        subject = None
    if (request.POST.get('sub_subject') != None):
        sub_subject = Sub_subject.objects.get(id=request.POST.get('sub_subject'))
    else:
        sub_subject = None
    if (request.POST.get('manipulation') != None):
        manipulation = Manipulation.objects.get(id=request.POST.get('manipulation'))
    else:
        manipulation = None
    if (request.POST.get('hospital') != None):
        hospital = Hospital.objects.get(id=request.POST.get('hospital'))
    else:
        hospital = None
    if (request.POST.get('city') != None):    
        city = City.objects.get(id=request.POST.get('city'))
    else:
        city = None
    question = request.POST.get('question')
    if (request.POST.get('street') != None):
        street = request.POST.get('street')
    else:
        street = None
    if (request.POST.get('number') != None):
        number = request.POST.get('number')
    else:
        number = None
    if (request.POST.get('building') != None):    
        building = request.POST.get('building')
    else:
        building = None
    if (request.POST.get('room') != None):
        room = request.POST.get('room')
    else:
        room = None
    # if (request.POST.get('patient_fio') != None):
    #     patient_fio = request.POST.get('patient_fio')
    # else:
        # patient_fio = None
    if (request.POST.get('registration_covid_date') == ''): 
         registration_covid_date = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
    else:
         registration_covid_date = datetime.datetime.strptime(request.POST.get('registration_covid_date').strip(), '%d.%m.%Y').isoformat()    
    if (request.POST.get('callback_number') != None):
        callback_number = request.POST.get('callback_number').strip()
    else:
        callback_number = None
    if (request.POST.get('call_result') != None):
        call_result = Hospital.objects.get(id=request.POST.get('call_result'))
    else:
        call_result = None
    if (request.POST.get('complited') == 'on'):
        complited = True
    elif (request.POST.get('complited') == 'off'):
        complited = False
    else:
        complited = False 
    if (request.POST.get('urgent') == 'on'):
        urgent = True
    elif (request.POST.get('urgent') == 'off'):
        urgent = False 
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
    patient_fio_array = request.POST.getlist('patient_fio[]')
    patient_date_of_birth = request.POST.getlist('date_of_birth[]')
    for i in range(0,int(request.POST.get('total_forms'))):
        if (patient_fio_array[i] != None): 
            if(patient_date_of_birth[i] == '' ):
                    date_of_birth = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
            else:
                date_of_birth = datetime.datetime.strptime(patient_date_of_birth[i].strip(), '%d.%m.%Y').isoformat()
            patient = Patient(
                patient_fio=patient_fio_array[i],
                date_of_birth=date_of_birth,
                call=call
            )
            patient.save()
            
    journal_create_call = call
    journal_create_message = f'запись о вызове создана'
    journal_create_date = datetime.datetime.now().isoformat()
    journal_create = Journal(
        call = journal_create_call,
        date = journal_create_date,
        message = journal_create_message,
    )
    journal_create.save()
    if call.hospital and call.hospital.email:
        utils.DNS_NAME._fqdn = "122.egov66.ru"
        
        # call_number = call.call_number
        # call_date = call.date
        # message = get_template("emails/call_notification.html").render(Context({
        #     'call_number': call_number,
        #     'call_date': call_date
        # }))
        message = f'в службу 112 поступило в {call.date} от номера {call.call_number}'
        if call.subject:
            message += f'Тема обращения {call.subject.name} \n'
        message += f'суть обращения {call.question} \n'
        message += f'просим связаться с заявителем и оказать ему помощь, '
        message += f'более подробная информация предоставлена на странице вашей больницы \n'
        message += f'https://122.egov66.ru/hospital/call/{call.id}  \n'
        message += f'ваш логин это первая чать вашего email адреса \n'
        message += f'для получения пароля проидите пожалуйста процедуру сброса пароля'



        mail = EmailMessage(
            subject="122 Горячая линия",
            body=message,
            from_email=EMAIL_HOST_USER,
            to=[call.hospital.email],
            reply_to=[EMAIL_HOST_USER],
        )
        mail.content_subtype = "html"
        mail.send()
        journal_message=f'email отправлен на адрес {call.hospital.email}'
        journal_call = call
        journal_date = datetime.datetime.now().isoformat()
        journal = Journal(
            call=journal_call,
            message=journal_message,
            date=journal_date
        )
        journal.save()
    return HttpResponseRedirect("/")

@method_decorator(login_required, name='dispatch')
class HospitalListCalls(PermissionRequiredMixin, ListView):
    permission_required = 'calls.view_hospital'
    model = Call
    paginate_by = 10
    context_object_name = 'calls'
    template_name = "hospitals/index.html"
    def get_queryset(self):
        hospital = Hospital.objects.get(email=self.request.user.email)
        return Call.objects.filter(hospital=hospital).filter(active=True).select_related('call_result').order_by('-date')
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(HospitalListCalls, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        hospital = Hospital.objects.get(email=self.request.user.email)
        count = Call.objects.filter(hospital=hospital).filter(active=True).select_related('call_result').count()
        context['count'] = count
        context['hospital'] = hospital
        return context


 # @login_required
# @permission_required('calls.view_hospital')       
# def hospital_all(request):
#     hospital = Hospital.objects.get(email=request.user.email)
#     template = "hospitals/index.html"
#     calls = Call.objects.filter(hospital=hospital).filter(active=True).select_related('call_result').order_by('-date')
#     count = Call.objects.filter(hospital=hospital).filter(active=True).select_related('call_result').count()
#     paginator = Paginator(calls,10)
#     page = request.GET('page')
#     try:
#         calls = paginator.page(page)
#     except PageNotAnInteger:
#         calls = paginator.page(1)
#     except EmptyPage:
#         calls = paginator.page(paginator.num_pages)
    
#     context = {
#         "hospital": hospital.name,
#         "calls": calls,
#         "count": count,
#     }
#     return render(request,template,context)

# @login_required
# @permission_required('calls.view_hospital')
# def hospital_show(request, id):
#     template = 'hospitals/show.html'
#     call = Call.objects.get(pk=id)
#     patient = Patient.objects.filter(call=call)
#     journals = Journal.objects.filter(call=call)
#     context = {
#         'call': call,
#         'patient': patient,
#         'journals': journals,
#     }
#     return render(request, template, context)

@method_decorator(login_required, name='dispatch')
class HospitalShowCall(PermissionRequiredMixin, DetailView):
    permission_required = 'calls.view_hospital'
    model = Call
    context_object_name = 'call'
    template_name = 'hospitals/show.html'
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(HospitalShowCall, self).get_context_data(**kwargs)
        call = Call.objects.get(pk=self.kwargs.get('pk'))
        patients = Patient.objects.filter(call=call)
        journals = Journal.objects.filter(call=call)
        context['patients'] = patients
        context['journals'] = journals
        return context

@login_required
@permission_required('calls.view_hospital')
def hospital_complite(request, id):
    call = Call.objects.get(pk=id)
    hospital = Hospital.objects.get(email=request.user.email)
    call.active = False
    call.save()
    journal_date = datetime.datetime.now().isoformat()
    journal_message = f'Пользователь {request.user} избольницы {hospital.name} обновил запись'
    journal = Journal(
        call=call,
        message=journal_message,
        date=journal_date,
    )
    journal.save()

    return redirect('calls:hospital_all')

@login_required
@permission_required('calls.view_hospital')
def hospital_wrong(request, id):
    call = Call.objects.get(pk=id)
    hospital = Hospital.objects.get(email=request.user.email)
    call.hospital = None
    call.urgent = True
    call.save()
    journal_date = datetime.datetime.now().isoformat()
    journal_message = f'Пользователь {request.user} избольницы {hospital.name} обновил запись '
    journal_message += f'данная запись ошибочно отнесена к этой больнице. \n'
    journal_message += f'Будет рассмотрена старшим опретором'
    journal = Journal(
        call=call,
        message=journal_message,
        date=journal_date,
    )
    journal.save()

    return redirect('calls:hospital_all')

# @login_required
# def list_all(request):
#     cursor = connections['pbx'].cursor()
#     busy = "'BUSY'"
#     cursor.execute(f'SELECT * FROM asterisk.hist2 WHERE "DIALSTATUS"={busy}  and abandoned')
#     raw = cursor.fetchall()
#     cursor2 = connections['pbx'].cursor()
#     cursor2.execute('SELECT count(*) as cnALL FROM asterisk.hist2 WHERE abandoned and dt::date=current_date')
#     raw2 = cursor2.fetchone()

#     print(raw)
#     #calls = Call.objects.filter(call_operator=request.user).select_related('call_result').order_by('-date')[:10]
#     template = 'list/index.html'
#     context = {
#         'calls': raw,
#         'count': raw2[0]
#     }
#     return render(request, template, context)

@login_required
def add_new(request):
    template = 'calls/add_new.html'
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

def load_sub_subject(request):
    subject_id = request.GET.get('subject')
    sub_subject = Sub_subject.objects.filter(subject=subject_id).order_by('name')
    response= {
        'data': sub_subject
    }
    return JsonResponse(response)