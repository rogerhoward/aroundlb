import os, pipes, json

from django.conf import settings
from celery import shared_task

from core.tools.misc import *

# import core.tools.media as media
# import core.tools.misc as misc
# import core.tools.md5 as md5

import PIL


def extract_metadata(file, options='groupedsimple', format='json'):
    print('extract_metadata: {}'.format(file))
    if os.path.isfile(file):
        exiftool_defaults = ' -m '

        option_string = ''
        if options == 'groupedsimple':
            option_string += '-G -s -s -g -n '
        if format == 'json':
            option_string += '-json '

        command_string = settings.EXIFTOOL_PATH + exiftool_defaults + option_string + pipes.quote(file)
        # print command_string
        metaobj = os.popen(command_string).read()
        # print metaobj
        if format == 'json':
            option_string += '-json '
            return json.loads(metaobj)
        else:
            return metaobj
    else:
        return False



def preview_img(in_path, out_path):
    print 'preview_img: %s' % (in_path)

    try:
        original = PIL.Image.open(in_path)
    except:
        print "Unable to load PIL.Image"
        return False

    original.thumbnail(settings.PREVIEW_SIZE)
    preview = original.filter(PIL.ImageFilter.UnsharpMask(radius=1.2, percent=150, threshold=4))
    preview.save(out_path, optimize=True, quality=settings.PREVIEW_QUALITY, progressive=True)

    return out_path


def preview_raw(in_path, out_path):
    print 'preview_raw: %s' % (in_path)
    command_string =  '%sconvert %s -filter Lanczos -sampling-factor 1x1 -resize %s -unsharp 1.5x1+0.5+0.02 -quality %s %s' % (settings.IMAGEMAGICK_PATH, pipes.quote(in_path), settings.PREVIEW_SIZE[0], settings.PREVIEW_QUALITY, pipes.quote(out_path))
    metaobj = os.popen(command_string).read()
    print command_string
    return out_path


def previewing(in_path, out_path):
    print 'previewing.....'
    print 'in_path: %s' % (in_path)
    print 'out_path: %s' % (out_path)
    mapping = {
        'tif': preview_raw,
        'png': preview_raw,
        'jpg': preview_raw,
        'dng': preview_raw,
        'cr2': preview_raw,
        'arw': preview_raw,
    }

    extension = misc.get_extension(in_path)
    print 'extension: %s' % (extension)
    converted = mapping[extension](in_path, out_path)

    return True
