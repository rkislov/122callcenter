import email
from email import message
from multiprocessing import context
from pyexpat import model
from re import template
from unittest.mock import call
from django.shortcuts import redirect, render, get_list_or_404
from django.contrib.auth.decorators import login_required
from calls.models import Journal, Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
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




@method_decorator(login_required, name='dispatch')
class SuperviserShowCall(PermissionRequiredMixin, ListView):
    permission_required = 'calls.change_call'
    model = Call
    paginate_by = 10
    context_object_name = 'calls'
    template_name = "supervisers/index.html"
    def get_queryset(self):
        #hospital = Hospital.objects.get(email=self.request.user.email)
        return Call.objects.select_related('call_result').order_by('-date')
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(SuperviserShowCall, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        count = Call.objects.select_related('call_result').count()
        context['count'] = count
        #context['hospital'] = hospital
        return context

@method_decorator(login_required, name='dispatch')
class SuperviserShow(PermissionRequiredMixin, DetailView):
    permission_required = 'calls.change_call'
    model = Call
    context_object_name = 'call'
    template_name = 'supervisers/show.html'
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(SuperviserShow, self).get_context_data(**kwargs)
        call = Call.objects.get(pk=self.kwargs.get('pk'))
        patients = Patient.objects.filter(call=call)
        journals = Journal.objects.filter(call=call)
        context['patients'] = patients
        context['journals'] = journals
        return context


@method_decorator(login_required, name='dispatch')
class SuperviserEdit(PermissionRequiredMixin, DetailView):
    permission_required = 'calls.change_call'
    model = Call
    context_object_name = 'call'
    template_name = 'supervisers/edit.html'
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(SuperviserEdit, self).get_context_data(**kwargs)
        call = Call.objects.get(pk=self.kwargs.get('pk'))
        patients = Patient.objects.filter(call=call)
        subjects = Subject.objects.all()
        manipulations = Manipulation.objects.all()
        hospitals = Hospital.objects.all()
        citys = City.objects.all()
        context['subjects'] = subjects
        context['manipulations'] = manipulations
        context['hospitals'] = hospitals
        context['patients'] = patients
        context['citys'] = citys
        return context


@login_required
def update(request):
    # date = datetime.datetime.now().isoformat()
    # call_number = request.POST.get('call_number').strip()
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
    call=Call.objects.get(pk=request.POST.get('callid'))
    
        # date=date,
        # call_number=call_number,
    call.subject=subject,
    call.sub_subject=sub_subject,
    call.registration_covid_date=registration_covid_date,
    call.manipulation=manipulation,
    call.hospital=hospital,
    call.city=city,
    call.question=question,
    # call.address=address,
    call.callback_number=callback_number,
    call.call_result=call_result,
    call.call_operator=call_operator,
    call.complited=complited,
    call.urgent=urgent,
    call.active=active,
    
    call.save()
    patients_array = Patient.objects.filter(call=call)
    patient_fio_array = request.POST.getlist('patient_fio[]')
    patient_date_of_birth = request.POST.getlist('date_of_birth[]')
    for i in range(0,int(request.POST.get('total_forms'))):
        if (patient_fio_array[i] != None): 
            for ii in range(0, int(patients_array)):
                if(patient_date_of_birth[i] == '' ):
                        date_of_birth = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
                else:
                    date_of_birth = datetime.datetime.strptime(patient_date_of_birth[i].strip(), '%d.%m.%Y').isoformat()
                    patient=Patient.objects.get(patient[ii])
                    patient.patient_fio=patient_fio_array[i]
                    patient.date_of_birth=date_of_birth
                    patient.save()
            if (patient_fio_array[i] != None): 
                if(patient_date_of_birth[i] == '' ):
                        date_of_birth = datetime.datetime.strptime('01.01.1900', '%d.%m.%Y').isoformat()
                else:
                    date_of_birth = datetime.datetime.strptime(patient_date_of_birth[i].strip(), '%d.%m.%Y').isoformat()
                    patient.patient_fio=patient_fio_array[i]
                    patient.date_of_birth=date_of_birth
                patient = Patient(
                    patient_fio=patient_fio_array[i],
                    date_of_birth=date_of_birth,
                    call=call
                )
                patient.save()
    address = Address.objects.get(call=call)

    address.street=street,
    address.number=number,
    address.building=building,
    address.room=room
    address.save()

    call.address=address
    call.save()
    journal_update_call = call
    journal_update_message = f'запись о вызове обновлена'
    journal_update_date = datetime.datetime.now().isoformat()
    journal_update = Journal(
        call = journal_update_call,
        date = journal_update_date,
        message = journal_update_message,
    )
    journal_update.save()
    if call.hospital and call.hospital.email:
        utils.DNS_NAME._fqdn = "122.egov66.ru"
        
        # call_number = call.call_number
        # call_date = call.date
        # message = get_template("emails/call_notification.html").render(Context({
        #     'call_number': call_number,
        #     'call_date': call_date
        # }))
        message = f'в службе 112 обновлена в {call.date} инфлрмация о звонке от номера {call.call_number}'
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


