from django.urls import path

from . import views


app_name = "calls"

urlpatterns = [
    # Главная страница
    path('', views.index, name='main'),
    path('call/add', views.add, name='add'),
    path('call/save', views.save, name='save'),
    path('call/<int:id>', views.show, name='show'),
    path('ajax/load_sub_subject/', views.load_sub_subject, name='ajax_load_sub_subject'),
]
