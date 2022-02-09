from django.contrib import admin
from .models import Videocall

# Register your models here.
class VideacallAdmin(admin.ModelAdmin):
    list_display =(
        'pk',
        'date',
        'date_of_call',
        'url_str',
        'request',
        'accepted',
        'success',
        'nomer_bolnichnogo'
    )
    list_filter = (
        'date',
        'date_of_call',
        'url_str',
        'request',
        'accepted',
        'success',
        'nomer_bolnichnogo'
        )
    empty_value_display = '-пусто-'

admin.site.register(Videocall, VideacallAdmin)
