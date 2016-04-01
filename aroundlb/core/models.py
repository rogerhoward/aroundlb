from __future__ import unicode_literals

import uuid
import os
import simplejson as json

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

import core.tools.media as media
import core.tools.misc as misc
import core.tools.md5 as md5

# from core.tasks import *

from PIL import Image
from PIL import ImageFilter
from pipes import quote


# --------------------------------------------------
# Abstract base classes
# --------------------------------------------------

class GenericBaseClass(models.Model):
    """
    The standard abstract base class for primary classes provides basic fields and infrastructure for
    all Model classes in this project
    """
    datetime_updated = models.DateTimeField(auto_now=True, null=True, blank=True, db_index = True, help_text='The datetime this actual object was updated.', )

    class Meta:
        abstract = True
        get_latest_by = "datetime_updated"

# --------------------------------------------------
# Core Classes
# --------------------------------------------------

class Asset(GenericBaseClass):
    """
    Represents unique Assets.
    """
    original = models.ImageField(null=True, blank=True, upload_to='originals/', height_field='original_height', width_field='original_width', max_length=256)
    original_width = models.IntegerField(null=True, blank=True, db_index=True, )
    original_height = models.IntegerField(null=True, blank=True, db_index=True, )
    md5 = models.CharField(null=True, blank=True, db_index=True, max_length=32, )
    metadata = models.OneToOneField('Metadata', related_name='asset', null=True, blank=True)

    title = models.TextField(null=True, blank=True, help_text='Displayable title', )
    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, )

    class Meta:
        get_latest_by = 'datetime_updated'
        ordering = ['-datetime_updated', ]

    def __unicode__(self):
        if self.original:
            return u'%s' % (self.original.url)
        else:
            return u'(%s)' % (self.pk)
    
    @property
    def path(self):
        if self.original:
            return os.path.join(settings.MEDIA_ROOT, self.original.url)
        else:
            return False

    def save(self, *args, **kwargs):
        print('saving asset...')
        super(Asset, self).save(*args, **kwargs)


class Metadata(GenericBaseClass):
    """
    Represents unique Metadata.
    """
    content = models.TextField(
                                null=True, 
                                blank=True, 
                                help_text='Displayable title', )
    md5 = models.CharField(
                            null=True, 
                            blank=True, 
                            db_index=True, 
                            max_length=32, )

    def update(self):
        print 'updating metadata for %s' % (self.asset)

        metadata_response = media.extract_metadata(self.asset.path)
        if metadata_response:
            self.content = metadata_response
            print metadata_response
            self.md5 = md5.getmd5(metadata_response)
            return True
        else:
            return False




@receiver(post_save, sender=Asset)
def create_metadata_for_new_assets(sender, instance, created, **kwargs):
    if created:
        md = Metadata(asset=instance)
        md.save()


@receiver(pre_save, sender=Metadata)
def import_metadata_on_create(sender, instance, **kwargs):
    instance.update()