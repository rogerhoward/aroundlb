from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

def home(request):
    return render(request, 'vr.html', {
        'modules': settings.CUSTOM_APPS,
    })

def home2(request):
    return render(request, 'vr2.html', {
        'modules': settings.CUSTOM_APPS,
    })
