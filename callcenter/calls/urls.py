from os import name
from django.urls import path

from . import views


app_name = "calls"

urlpatterns = [
    # Главная страница
    path('', views.index, name='main'),
    path('call/add', views.add, name='add'),
    path('call/save', views.save, name='save'),
    path('call/<int:id>', views.show, name='show'),
   # path('hospital/all', views.hospital_all, name='hospital_all'),
    path('hospital/all/', views.HospitalListCalls.as_view(), name='hospital_all'),
    #path('hospital/call/<int:id>', views.hospital_show, name='hospital_show'),
    path('hospital/call/<int:pk>', views.HospitalShowCall.as_view(), name='hospital_show'),
    path('hospital/call/<int:id>/complite', views.hospital_complite, name='hospital_complite'),
    path('hospital/call/<int:id>/wrong', views.hospital_wrong, name='hospital_wrong'),
    path('list/all', views.list_all, name='list_all'),
]
