from django.urls import path
from . import views


app_name = "video"

urlpatterns = [
    path('', views.index, name='main'),
    path('generate_url_patient', views.generate_link_patient, name="generate_link_patient" ),
    path('patient/<str:url_str>', views.patient_video, name="patient_room"),
    path('doctor/<str:url_str>', views.doctor_video, name="doctor_room")
]
