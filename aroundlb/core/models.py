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


class DescriptiveBaseClass(GenericBaseClass):
    """
    The standard abstract base class for primary classes provides basic fields and infrastructure for
    all Model classes in this project
    """

    title = models.TextField(null=True, blank=True, help_text='Displayable title', )
    description = models.TextField(null=True, blank=True, help_text='Description', )
    name = models.CharField(null=False, blank=False, unique=True, db_index=True, max_length=255, help_text='Unique name for this object', )
    type = models.CharField(null=True, blank=True, db_index=True, max_length=32, )

    class Meta:
        abstract = True
        get_latest_by = "datetime_updated"

# --------------------------------------------------
# Core Classes
# --------------------------------------------------

class Panorama(DescriptiveBaseClass):
    """
    Represents a Panorama, which may contain multiple assets.
    """
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True,)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True,)

    class Meta:
        get_latest_by = 'datetime_updated'
        ordering = ['-datetime_updated', ]

    def __unicode__(self):
        if self.title:
            return '{}'.format(self.title)
        else:
            return '({})'.format(self.name)


class Asset(DescriptiveBaseClass):
    """
    Represents unique Assets.
    """
    original = models.ImageField(null=True, blank=True, upload_to='originals/', height_field='original_height', width_field='original_width', max_length=256, )
    original_width = models.IntegerField(null=True, blank=True, db_index=True, )
    original_height = models.IntegerField(null=True, blank=True, db_index=True, )
    original_md5 = models.CharField(null=True, blank=True, db_index=True, max_length=32, )

    panorama = models.ForeignKey('Panorama', related_name='assets', null=True, blank=True,on_delete=models.CASCADE, )
    metadata = models.OneToOneField('Metadata', related_name='asset', null=True, blank=True, )

    class Meta:
        get_latest_by = 'datetime_updated'
        ordering = ['-datetime_updated', ]

    def __unicode__(self):
        if self.original:
            return '{}'.format(self.original.url)
        else:
            return '({})'.format(self.pk)
    
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
        print 'updating metadata...'

        # metadata_response = media.extract_metadata(self.asset.path)
        # if metadata_response:
        #     self.content = metadata_response
        #     print metadata_response
        #     self.md5 = md5.getmd5(metadata_response)
        #     return True
        # else:
        #     return False




# @receiver(post_save, sender=Asset)
@receiver(pre_save, sender=Asset)
def create_metadata_for_new_assets(sender, instance, **kwargs):
    if not instance.metadata:
        md = Metadata()
        md.save()
        instance.metadata = md



@receiver(pre_save, sender=Metadata)
def import_metadata_on_create(sender, instance, **kwargs):
    instance.update()