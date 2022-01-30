from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call, Journal

class CallResource(resources.ModelResource):

    class Meta:
        model = Call


class CallAdmin(ImportExportModelAdmin):
     # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'pk',
        'date',
        'call_number',
        'question',
        'hospital',
        'call_result',
        'manipulation',
        'registration_covid_date',
        'subject',
        'sub_subject',
        )
    list_filter = (
        'date',
        'hospital',
        'subject',
        'sub_subject',
        'manipulation',
        'call_result',
        'registration_covid_date',
        'subject',
        'sub_subject',
        )
    # # Добавляем интерфейс для поиска по тексту постов
    # search_fields = (
    #     'call_number',
    #     'date',
    #     'hospital',
    #     )
    # Добавляем возможность фильтрации по дате
    list_filter = (
        'date',
        'subject',
        'sub_subject',
        'hospital',
        'manipulation'
        )
    # Это свойство сработает для всех колонок: где пусто — там будет эта строка
    empty_value_display = '-пусто-'
    resource_class = CallResource


class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'email'
    )

admin.site.register(Subject)
admin.site.register(Sub_subject)
admin.site.register(Patient)
admin.site.register(Manipulation)
admin.site.register(City)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Call_result)
admin.site.register(Address)
admin.site.register(Journal)
admin.site.register(Call, CallAdmin)
