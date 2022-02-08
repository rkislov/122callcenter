from unittest import result
from django.db import models

from django.db import models
from django.contrib.auth.models import User



class Videocall(models.Model):
    ''' Модель описывающая подтип обращения'''
    date = models.DateTimeField(auto_now_add=True)
    date_of_call = models.DateTimeField(default=None),
    url = models.CharField(max_length=30, default=None),
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='videocall_patient',
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='videocall_doctor'
    )
    request = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    nomer_bolnichnogo = models.CharField(max_length=20, blank=True, null=True)

    

    def __str__(self):
        '''Функция возвращает название'''
        return self.url
    
