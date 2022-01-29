from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    ''' Модель описывающая подтип обращения'''
    name = models.CharField(max_length=200, help_text="Введите причину обращения")

    def __str__(self):
        '''Функция возвращает название'''
        return self.name


class Sub_subject(models.Model):
    ''' Модель описывающая тип обращения'''
    name = models.CharField(max_length=200, help_text="Введите подпричину обращения")
    genre = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
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
    number = models.CharField(max_length=10, help_text="Введите номер дома", null=True)
    building = models.CharField(max_length=10, help_text="Введите номер строения", null=True)
    room = models.CharField(max_length=10, help_text="Введите номер квартиры", null=True)

    def __str__(self):
        '''возвращает строку адреса'''
        return 'ул.%s, д.%s, корп.%s, кв.%s' % (self.street, self.number, self.building, self.room)


class Hospital(models.Model):
    '''Модель описывающая названия'''
    name = models.CharField(max_length=200, help_text="Введите сокращенное название МО")

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
    call_number = models.CharField(max_length=11, help_text="Введите номер с которого звонили")
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True
    )
    sub_subject = models.ForeignKey(
        Sub_subject,
        on_delete=models.SET_NULL,
        null=True
    )
    callback_number = models.CharField(max_length=11, help_text="Введите номер с которого для обратной связи")
    question = models.TextField()
    registration_covid_date = models.DateTimeField(null=True,blank=True)
    manipulation = models.ForeignKey(
        Manipulation,
        on_delete=models.SET_NULL,
        null=True
    )
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True
    )
    call_result = models.ForeignKey(
        Call_result,
        on_delete=models.SET_NULL,
        null=True
    )
    call_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Patient(models.Model):
    ''' Модель описывающая пациента обращения'''
    patient_fio = models.CharField(max_length=400, help_text="Введите ФИО пациента")
    date_of_birth = models.DateTimeField(null=True, blank=True)
    call = models.ForeignKey(
        Call,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        '''Функция возвращает название'''
        return self.patient_fio
    
