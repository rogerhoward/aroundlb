import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.models import Asset

class Command(BaseCommand):
    args = '<dir>'
    help = 'Synchronizes the app with file system.'



    def metadataUpdate(self, assets):
        # Removes all missing files within a path from the database
        print 'begin metadataUpdate with %s' % (assets.count())
        for this_asset in assets:
            this_asset.update_metadata()

    # def add_arguments(self, parser):
    #     parser.add_argument('--input')

    def handle(self, *args, **options):
        print 'exiftool begin'
        print options
        # input_file = options['input']
        assets = Asset.objects.all()
        self.metadataUpdate(assets)