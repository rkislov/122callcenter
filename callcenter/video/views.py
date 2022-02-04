from re import template
from django.shortcuts import render




def index(request):
    template = 'video/index.html'
    context = {
        'name': 'test'
    }
    return render(request, template, context)

    