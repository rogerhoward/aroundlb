from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Asset, Panorama, Metadata


def home(request):
    return render(request, 'map.html', {
        'modules': settings.CUSTOM_APPS,
    })


def panoramas(request):
    these_panos = Panorama.objects.all()
    pano_array = map(lambda p: p.json, these_panos)
    return JsonResponse(pano_array, safe=False)