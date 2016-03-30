from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from core.tools.misc import *
from PIL import Image, ImageFilter
import os
from pipes import quote

# from core.models import Asset, Metadata


# @shared_task
# def metadata_for_asset(path_md5):
#     pass

@shared_task
def preview_img(in_path, out_path):
    print 'preview_img: %s' % (in_path)
    try:
        original = Image.open(in_path)
    except:
        print "Unable to load image"
        return False
    original.thumbnail(settings.PREVIEW_SIZE)
    preview = original.filter(ImageFilter.UnsharpMask(radius=1.2, percent=150, threshold=4))
    preview.save(out_path, optimize=True, quality=settings.PREVIEW_QUALITY, progressive=True)
    return out_path


@shared_task
def preview_raw(in_path, out_path):
    print 'preview_raw: %s' % (in_path)
    command_string =  '%sconvert %s -filter Lanczos -sampling-factor 1x1 -resize %s -unsharp 1.5x1+0.5+0.02 -quality %s %s' % (settings.IMAGEMAGICK_PATH, quote(in_path), settings.PREVIEW_SIZE[0], settings.PREVIEW_QUALITY, quote(out_path))
    metaobj = os.popen(command_string).read()
    print command_string
    return out_path


@shared_task
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

    extension = get_extension(in_path)
    print 'extension: %s' % (extension)
    converted = mapping[extension](in_path, out_path)

    return True

