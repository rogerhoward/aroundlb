from django.contrib import admin
from models import Asset, Metadata

class AssetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Asset, AssetAdmin)

class MetadataAdmin(admin.ModelAdmin):
    pass
admin.site.register(Metadata, MetadataAdmin)