import os
# from core.tools.misc import *
import core.tools.md5 as md5
import core.tools.misc as misc
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from core.models import Asset

class Command(BaseCommand):
    args = '<dir>'
    help = 'Synchronizes the app with file system.'

    def AddAllFiles(self, path):
        # Adds all files within a path to the database
        print 'begin AddAllFiles with %s' % (path)
        for directory, directories, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(directory, filename)
                if misc.get_extension(filename) in settings.ALLOWED_EXTENSIONS:
                    this_path_md5 = md5.getmd5(file_path)
                    this_asset, created = Asset.objects.get_or_create(file_path_md5=this_path_md5, file_path = file_path)
                    print 'adding... %s' % (file_path)
                    this_asset.file_path = file_path
                    this_asset.save()



    def RemoveMissingFiles(self, path):
        # Removes all missing files within a path from the database
        print 'begin RemoveMissingFiles with %s' % (path)
        for this_asset in Asset.objects.all():
            if os.path.isfile(this_asset.file_path):
                # print 'file exists... %s' % (this_asset.file_path)
                pass
            else:
                print 'file does not exist... %s' % (this_asset.file_path)
                this_asset.delete()


    def filesystemUpdate(self, path):
        # (re)synchronizes an entire path with the database
        print 'begin filesystemUpdate with %s' % (path)
        self.AddAllFiles(path)
        # self.RemoveMissingFiles(path)

    def add_arguments(self, parser):
        parser.add_argument('--input')

    def handle(self, *args, **options):
        print 'fsync begin'
        print options

        settings.PREVIEW_UPDATE_ON_SAVE = False
        settings.METADATA_UPDATE_ON_SAVE = False

        input_file = options['input']
        self.filesystemUpdate(input_file)