import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import boto3
from pipes import quote

class Command(BaseCommand):
    args = '<dir>'
    help = 'Testing convert.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file')

    def make_pano(in_path):
        print 'make_pano: %s'.format(in_path)

        data = {'bin': settings.KRPANO_BIN, 
                'template': settings.KRPANO_TEMPLATE, 
                'input': in_path
                }
                
        command_string =  '{bin} makepano -config={template} {input}'.format(*data)
        metaobj = os.popen(command_string).read()
        print command_string
        return out_path


    def handle(self, *args, **options):
        print options