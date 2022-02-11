from django.urls import path

from . import views


app_name = "profiles"


urlpatterns = [
    path('lk/', views.DoctorShow.as_view(), name='lk'),
    path('accept/<int:id>/', views.accept, name='accept'),
    path('finish/<str:url_str>/', views.finish, name='finish'),
]
