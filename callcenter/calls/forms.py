from django import forms
from .models import Call,Subject,Sub_subject,Patient,Hospital

class AddForm(forms.Form):
    model=Call