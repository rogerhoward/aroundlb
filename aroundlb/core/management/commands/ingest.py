import os
from django.core.management.base import BaseCommand, CommandError
from core.models import Asset, Metadata, Panorama
from django.conf import settings
import boto3, pipes

class Command(BaseCommand):
    args = '<dir>'
    help = 'Testing ingest.'

    def process_panorama_directory(self, path):
        print 'process_panorama_directory: {}'.format(path)

        panorama_files = os.listdir(path)
        pts_scripts = [s for s in panorama_files if s.endswith('pts')]

        if len(pts_scripts) == 0:
            return False

        this_pts = pts_scripts[0]

        this_identifier = this_pts.split('-')[0]
        print('this_identifier: {}'.format(this_identifier))

        this_panorama, created = Panorama.objects.get_or_create(
            name=this_identifier,
            defaults={'title': os.path.basename(path), 'type':'panorama'},
        )
        print(this_panorama)

        # if created:
        #     # means you have created a new person
        # else:
        #     # person just refers to the existing one


        # pano_tif_name = [s for s in panorama_files if s.endswith('pano.tif')][0]
        # pano_tif = os.path.join(path, pano_tif_name)
        # pano_jpg = os.path.join('/Users/rogerhoward/Desktop/', pano_tif_name.replace('tif', 'jpg'))
        # print pano_tif, pano_jpg
        # self.make_jpeg(pano_tif, pano_jpg)


    def make_jpeg(self, in_path, out_path):
        print('make_jpeg: {}'.format(in_path))

        data = {'magick': settings.IMAGEMAGICK_PATH, 'quality': 90, 'input':  pipes.quote(in_path), 'output': pipes.quote(out_path)}
        print(data)

        command_string =  '{magick}convert {input} -quality {quality} {output}'.format(**data)
        print(command_string)
        metaobj = os.popen(command_string).read()

        return out_path



    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file')

    def handle(self, *args, **options):
        # print options
        self.process_panorama_directory(options['file'])