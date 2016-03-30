from django.contrib import admin
from models import Asset, Round, Metadata

class RoundAdmin(admin.ModelAdmin):
    pass
admin.site.register(Round, RoundAdmin)