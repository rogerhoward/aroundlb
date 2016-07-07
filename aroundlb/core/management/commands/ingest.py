import os
from django.core.management.base import BaseCommand, CommandError
from core.models import Asset, Metadata, Panorama
import core.tools.media
from django.conf import settings
import boto3, pipes
import arrow

class Command(BaseCommand):
    args = '<dir>'
    help = 'Testing ingest.'

    def process_panorama_directory(self, path):
        print 'process_panorama_directory: {}'.format(path)

        panorama_files = os.listdir(path)
        pts_scripts = [s for s in panorama_files if s.endswith('.pts')]
        tiff_images = [os.path.join(path, s) for s in panorama_files if s.endswith('.tif')]

        print('tiff_images: {}'.format(tiff_images))

        if len(pts_scripts) == 0:
            return False

        this_pts = pts_scripts[0]

        this_identifier = this_pts.split('-')[0]
        print('this_identifier: {}'.format(this_identifier))

        this_panorama, created = Panorama.objects.get_or_create(
            name=this_identifier,
            defaults={'title': os.path.basename(path)},
        )
        this_panorama.save()


        print('extract_metadata 1: {}'.format(tiff_images[0]))
        this_metadata = core.tools.media.extract_metadata(tiff_images[0])[0]
        print(this_metadata['Composite'])

        if 'GPSLatitude' in this_metadata['Composite']:
            print('GPSLatitude: {}'.format(this_metadata['Composite']['GPSLatitude']))
            this_panorama.latitude = this_metadata['Composite']['GPSLatitude']

        if 'GPSLongitude' in this_metadata['Composite']:
            print('GPSLongitude: {}'.format(this_metadata['Composite']['GPSLongitude']))
            this_panorama.longitude = this_metadata['Composite']['GPSLongitude']

        originals_path = os.path.join(settings.MEDIA_ROOT, 'originals')

        if 'DigitalCreationDateTime' in this_metadata['Composite']:
            print('DigitalCreationDateTime: {}'.format(this_metadata['Composite']['DigitalCreationDateTime']))
            exiftool_time = this_metadata['Composite']['DigitalCreationDateTime']

            try:
                datetime_created = arrow.get(exiftool_time, 'YYYY:MM:DD HH:mm:ssZZ').datetime
            except:
                try:
                    datetime_created = arrow.get(exiftool_time, 'YYYY:MM:DD HH:mm:ss').datetime
                except:
                    datetime_created = None

            this_panorama.datetime_created = datetime_created


        print 'handling panos...'
        pano_tiffs = [s for s in panorama_files if s.endswith('pano.tif')]
        if len(pano_tiffs) > 0:
            pano_identifier = pano_tiffs[0].replace('.tif', '')
            in_path = os.path.join(path, pano_tiffs[0])
            out_path = os.path.join(originals_path, pano_tiffs[0].replace('.tif', '.jpg'))
            out_path_relative = os.path.relpath(out_path, settings.MEDIA_ROOT)

            self.make_jpeg(in_path, out_path)

            this_asset, created = Asset.objects.get_or_create(
                name=pano_identifier,
            )
            this_asset.original.name = out_path_relative
            this_asset.panorama = this_panorama
            this_asset.type = 'pano'
            this_asset.save()

        sphere_tiffs = [s for s in panorama_files if s.endswith('sphere.tif')]
        if len(sphere_tiffs) > 0:
            sphere_identifier = sphere_tiffs[0].replace('.tif', '')
            in_path = os.path.join(path, sphere_tiffs[0])
            out_path = os.path.join(originals_path, sphere_tiffs[0].replace('.tif', '.jpg'))
            out_path_relative = os.path.relpath(out_path, settings.MEDIA_ROOT)

            self.make_jpeg(in_path, out_path)

            this_asset, created = Asset.objects.get_or_create(
                name=sphere_identifier,
            )
            this_asset.original.name = out_path_relative
            this_asset.panorama = this_panorama
            this_asset.type = 'sphere'
            this_asset.save()

        planet_tiffs = [s for s in panorama_files if s.startswith(this_identifier+'planet') and s.endswith('.tif')]
        print planet_tiffs
        for this_planet in planet_tiffs:
            planet_identifier = this_planet.replace('.tif', '')
            in_path = os.path.join(path, this_planet)
            out_path = os.path.join(originals_path, this_planet.replace('.tif', '.jpg'))
            out_path_relative = os.path.relpath(out_path, settings.MEDIA_ROOT)

            self.make_jpeg(in_path, out_path)

            this_asset, created = Asset.objects.get_or_create(
                name=planet_identifier,
            )
            this_asset.original.name = out_path_relative
            this_asset.panorama = this_panorama
            this_asset.type = 'planet'
            this_asset.save()

        print 'this_panorama.save()'
        this_panorama.save()

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