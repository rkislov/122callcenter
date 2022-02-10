from os import name
from django.urls import path

from . import views


app_name = "hospitals"



urlpatterns = [
       # path('hospital/all', views.hospital_all, name='hospital_all'),
    path('all/', views.HospitalListCalls.as_view(), name='all'),
    #path('hospital/call/<int:id>', views.hospital_show, name='hospital_show'),
    path('call/<int:pk>', views.HospitalShowCall.as_view(), name='show'),
    path('call/<int:id>/complite', views.hospital_complite, name='complite'),
    path('call/<int:id>/wrong', views.hospital_wrong, name='wrong'),
    path('api/get/calls_hospital', views.ListCalls.as_view(), name="active_page"),
    path('api/get/call_result', views.getCallResult, name = "get_callresult"),
]
