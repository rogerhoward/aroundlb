from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

def home(request):
    return render(request, 'vr.html', {
        'modules': settings.CUSTOM_APPS,
    })
