from django.conf import settings


def global_settings(request):
    # return any necessary values
    return {
        'S3_URL_BASE': settings.S3_URL_BASE,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE
    }