from django.contrib import admin
from models import Asset, Metadata, Panorama

class PanoramaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Panorama, PanoramaAdmin)

class AssetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Asset, AssetAdmin)

class MetadataAdmin(admin.ModelAdmin):
    pass
admin.site.register(Metadata, MetadataAdmin)