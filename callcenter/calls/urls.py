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
    path('hospital/all', views.hospital_all, name='hospital_all'),
    path('hospital/call/<int:id>', views.hospital_show, name='hospital_show'),
]
