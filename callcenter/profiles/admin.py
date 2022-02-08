from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display =(
        'pk',
        'user',
        'snils',
        'medpolis',
        'mobile'
    )
    list_filter = (
        'user',
        'snils',
        'medpolis',
        'mobile',
        )
    empty_value_display = '-пусто-'


admin.site.register(Profile, ProfileAdmin)
