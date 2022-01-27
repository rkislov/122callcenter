from os import name
from django.urls import path
from . import views


app_name = "calls"

urlpatterns = [
    # Главная страница
    path('', views.index, name='main'),
    path('call/add', views.add, name='add'),
    path('call/save', views.save, name='save')
]
