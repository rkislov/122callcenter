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
import json
from django.core.serializers import serialize
from django.views import View




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

    return redirect('hospitals:all')

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

    return redirect('hospitals:all')

class ListCalls(View):
    page_limit = 10
    def get_paginated_context(self, queryset, page, limit):
        if not page:    page = 1 # if no page provided, set 1

        # if limit specified, set the page limit
        if limit:   
            self.page_limit = limit  

        # instantiate the paginator object with queryset and page limit
        paginator = Paginator(queryset, self.page_limit)
        # get the page object
        page_obj = paginator.get_page(page)
        # serialize the objects to json
        serialized_page = serialize("json", page_obj.object_list)
        # get only required fields from the serialized_page json.
        serialized_page = [obj["fields"] for obj in json.loads(serialized_page)]

        # return the context.
        return {
            "data": serialized_page,
            "pagination": {
                "page": page,
                "limit": limit,
                "has_next": page_obj.has_next(),
                "has_prev": page_obj.has_previous(),
                "total": queryset.count()
            }
        }

    '''
    GET method for this View.
    '''
    def get(self, request, *args, **kwargs):
        # fetch the query params
        page = request.GET.get('page')
        limit = request.GET.get('limit')
        active = request.GET.get('active')
        hospital = request.GET.get('hospital') 
        if (request.POST.get('start') == None): 
            start = ''
        else:
            start = datetime.datetime.strptime(request.POST.get('start'), '%d.%m.%Y').isoformat()    
        if (request.POST.get('end') == None): 
            end = ''
        else:
            end = datetime.datetime.strptime(request.POST.get('end'), '%d.%m.%Y').isoformat()    
        
       

        sort_by = request.GET.get('sort_by')
        # get all results from DB.
        queryset = Call.objects.all()
        #hospital = Hospital.objects.get(email=self.request.user.email)
        #Call.objects.pref_related('call_result')
        '''filter the queryset object based on query params'''
        # 1. on basis of country
        if active and active != "all":
            queryset = queryset.filter(active=active)
        # 2. On basis of date (start and end date)
        if start and end:
            if start != "0" and end != "0":
                queryset = queryset.filter(
                    date__gte = start, 
                    date__lte = end
                )

        # 3. Sorting the filtered queryset
        if sort_by and sort_by != "0":
            queryset = queryset.order_by(sort_by)
        
         # 3. Sorting the filtered queryset
        if hospital and hospital != "0":
            queryset = queryset.select(hospital=hospital)

        # return the serialized output by 
        # calling method 'get_paginated_context'
        to_return = self.get_paginated_context(queryset, page, limit)
        return JsonResponse(to_return, status = 200)

def getCallResult(request):
    # get Countries from the database 
    # excluding null and blank values
    if request.method == "GET":
        call_result = Call_result.objects.all().values_list('name').distinct()
        call_result = [c[0] for c in list(call_result)]

        return JsonResponse({
            "call_result": call_result, 
        }, status = 200)