import datetime
from email.policy import default
from django.core.mail import utils,EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import BooleanField
from django.template import Context
from django.template.loader import get_template
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from callcenter.settings import EMAIL_HOST_USER


class Subject(models.Model):
    ''' Модель описывающая подтип обращения'''
    name = models.CharField(max_length=200, help_text="Введите причину обращения")

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Sub_subject(models.Model):
    ''' Модель описывающая тип обращения'''
    name = models.CharField(max_length=200, help_text="Введите подпричину обращения")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='sub_subject'
        )

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Manipulation(models.Model):
    '''Модель оказания консультации'''
    name = models.CharField(max_length=200, help_text="Укажите вид консультации") 

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class City(models.Model):
    '''Модель описывающая названия городов'''
    name = models.CharField(max_length=200, help_text="Введите название города или поселка")

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Address(models.Model):
    '''Модель адреса'''
    street = models.CharField(max_length=100, help_text="Введите адрес", null=True)
    number = models.CharField(max_length=12, help_text="Введите номер дома", null=True)
    building = models.CharField(max_length=10, help_text="Введите номер строения", null=True)
    room = models.CharField(max_length=10, help_text="Введите номер квартиры", null=True)

    def __str__(self):
        '''возвращает строку адреса'''
        return 'ул.%s, д.%s, корп.%s, кв.%s' % (self.street, self.number, self.building, self.room)


class Hospital(models.Model):
    '''Модель описывающая названия'''
    name = models.CharField(max_length=200, help_text="Введите сокращенное название МО")
    email = models.EmailField(blank=True,null=True)

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Call_result(models.Model):
    '''Модель описывает результаты звонка'''
    name = models.CharField(max_length=50, help_text="Введите значение")

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Call(models.Model):
    '''Модель описывает звонк'''
    date = models.DateTimeField(auto_now_add=True)
    call_number = models.CharField(max_length=12, help_text="Введите номер с которого звонили")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    sub_subject = models.ForeignKey(
        Sub_subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sub_subject'
    )
    callback_number = models.CharField(max_length=11, help_text="Введите номер с которого для обратной связи")
    question = models.TextField()
    registration_covid_date = models.DateTimeField(null=True,blank=True)
    manipulation = models.ForeignKey(
        Manipulation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    call_result = models.ForeignKey(
        Call_result,
        on_delete=models.SET_NULL,
        null=True,
        related_name='call'
    )
    call_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='call'
    )
    complited = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    
    class Meta:
        permissions = (
            ("operator", "Оператор горячей линии"),
            ("super_operator", "Супервайзер горячей линии"),
            ("hospital_operator", "Оператор больницы"),
            )

class Patient(models.Model):
    '''Модель описывающая пациента обращения'''
    patient_fio = models.CharField(max_length=1000, help_text="Введите ФИО пациента")
    date_of_birth = models.DateTimeField(null=True, blank=True)
    call = models.ForeignKey(
        Call,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='call'
    )

    def __str__(self):
        '''Функция возвращает название'''
        return self.patient_fio

class Journal(models.Model):
    call = models.ForeignKey(
        Call,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='call_jornaled'
    )
    message=models.CharField(max_length=1000)
    date=models.DateTimeField(auto_now_add=True)
    



# @receiver(post_save, sender=Call)
# def hospital_notification(sender, instance, created, **kwargs):
#     journal_create_call = instance
#     journal_create_message = f'запись о вызове создана'
#     journal_create_date = datetime.datetime.now().isoformat()
#     journal_create = Journal(
#         call = journal_create_call,
#         date = journal_create_date,
#         message = journal_create_message,
#     )
#     journal_create.save()
#     if instance.hospital and instance.hospital.email:
#         utils.DNS_NAME._fqdn = "122.egov66.ru"
#         call = instance
#         # call_number = call.call_number
#         # call_date = call.date
#         # message = get_template("emails/call_notification.html").render(Context({
#         #     'call_number': call_number,
#         #     'call_date': call_date
#         # }))
#         message = f'в службу 112 поступило в {call.date} от номера {call.call_number}'
#         if call.subject:
#             message += f'Тема обращения {call.subject.name} '
#         message += f'суть обращения {call.question} '
#         message += f'просим связаться с заявителем и оказать ему помощь'
#         mail = EmailMessage(
#             subject="122 Горячая линия",
#             body=message,
#             from_email=EMAIL_HOST_USER,
#             to=[call.hospital.email],
#             reply_to=[EMAIL_HOST_USER],
#         )
#         mail.content_subtype = "html"
#         mail.send()
#         journal_message=f'email отправлен на адрес {call.hospital.email}'
#         journal_call = call
#         journal_date = datetime.datetime.now().isoformat()
#         journal = Journal(
#             call=journal_call,
#             message=journal_message,
#             date=journal_date
#         )
#         return journal_create.save() 