from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Subject, Sub_subject, Patient, Manipulation, City, Hospital, Call_result, Address, Call

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
        'manipulation'
        )
    list_filter = (
        'date',
        'hospital',
        'subject',
        'sub_subject',
        'manipulation',
        )
    resource_class = CallResource

admin.site.register(Subject)
admin.site.register(Sub_subject)
admin.site.register(Patient)
admin.site.register(Manipulation)
admin.site.register(City)
admin.site.register(Hospital)
admin.site.register(Call_result)
admin.site.register(Address)
admin.site.register(Call,CallAdmin)
