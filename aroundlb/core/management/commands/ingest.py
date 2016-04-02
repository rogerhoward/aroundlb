import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import boto3, pipes

class Command(BaseCommand):
    args = '<dir>'
    help = 'Testing ingest.'

    def process_panorama_directory(self, path):
        print path

        panorama_files = os.listdir(path)
        print panorama_files

        has_pts = len([s for s in panorama_files if s.endswith('pts')]) > 0
        if not has_pts:
            return False

        pano_tif_name = [s for s in panorama_files if s.endswith('pano.tif')][0]
        pano_tif = os.path.join(path, pano_tif_name)
        pano_jpg = os.path.join('/Users/rogerhoward/Desktop/', pano_tif_name.replace('tif', 'jpg'))
        print pano_tif, pano_jpg
        self.make_jpeg(pano_tif, pano_jpg)


    def make_jpeg(self, in_path, out_path):
        print 'make_jpeg: {}'.format(in_path)

        data = {'magick': settings.IMAGEMAGICK_PATH, 'quality': 90, 'input':  pipes.quote(in_path), 'output': pipes.quote(out_path)}
        print data

        command_string =  '{magick}convert {input} -quality {quality} {output}'.format(**data)
        print command_string
        metaobj = os.popen(command_string).read()

        return out_path



    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file')

    def handle(self, *args, **options):
        print options
        self.process_panorama_directory(options['file'])