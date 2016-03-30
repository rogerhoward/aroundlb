from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.models import Asset


class Command(BaseCommand):
    args = '<dir>'
    help = 'Synchronizes the app with file system.'

    def resave(self, assets):
        print 'begin resave with %s' % (assets.count())
        for this_asset in assets:
            this_asset.save()

    def handle(self, *args, **options):
        print 'exiftool begin'
        print options
        assets = Asset.objects.all()
        self.resave(assets)
