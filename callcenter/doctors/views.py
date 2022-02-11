
from django.shortcuts import render
from video.models import Videocall
import email
from email import message
from unittest.mock import call
from django.shortcuts import redirect, render, get_list_or_404
from calls.models import Journal, Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call 
import datetime
from profiles.models import Profile
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from callcenter.settings import EMAIL_HOST_USER
from django.core.mail import utils,EmailMessage
from django.db import connections
from django.db.models import Prefetch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin



@method_decorator(login_required, name='dispatch')
class DoctorShow(PermissionRequiredMixin, ListView):
    permission_required = 'video.view_videocall'
    model = Videocall
    paginate_by = 10
    context_object_name = 'vcalls'
    template_name = "doctors/index.html"
    def get_queryset(self):
        #hospital = Hospital.objects.get(email=self.request.user.email)
        return Videocall.objects.prefetch_related().order_by('-date')
    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(DoctorShow, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        count = Videocall.objects.count()
        context['count'] = count
        return context

@login_required
@permission_required('video.view_videocall')
def accept(request,id):
    videocall=Videocall.objects.get(pk=id)
    videocall.date_of_call=datetime.datetime.now().isoformat()
    videocall.accepted=True
    videocall.doctor=request.user
    videocall.save()
    utils.DNS_NAME._fqdn = "122.egov66.ru"
        
        # call_number = call.call_number
        # call_date = call.date
        # message = get_template("emails/call_notification.html").render(Context({
        #     'call_number': call_number,
        #     'call_date': call_date
        # }))
    message = f'''
            Уважаемый пациент вам назначена видеоконсультация, 
            для ее проведения мы просим перейти по ссылке:
            https://122.egov66.ru/video/patient/{videocall.url_str} 
    '''

    mail = EmailMessage(
        subject="122 Горячая линия",
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[videocall.patient.email],
        reply_to=[EMAIL_HOST_USER],
    )
    mail.content_subtype = "html"
    mail.send()
    return redirect('doctors:lk')

@login_required
@permission_required('video.view_videocall')
def finish(request, url_str):
    videocall=Videocall.objects.get(url_str=url_str)
    videocall.success = True
    videocall.save() 
    return redirect('doctors:lk')

