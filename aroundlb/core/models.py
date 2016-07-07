from __future__ import unicode_literals

import uuid
import os
import simplejson as json
import arrow

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
    order = models.IntegerField(null=False, blank=False, default=0, db_index=True, )
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
    latitude = models.FloatField(null=True, blank=True, db_index=True, )
    longitude = models.FloatField(null=True, blank=True, db_index=True, )
    datetime_created = models.DateTimeField(null=True, blank=True, db_index=True, )

    @property
    def json(self):
        _dict = {}
        _dict['latitude'] = self.latitude
        _dict['longitude'] = self.longitude
        _dict['title'] = self.title
        _dict['description'] = self.description

        return _dict

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
            return os.path.join(settings.MEDIA_ROOT, self.original.name)
        else:
            return False

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
        print('metadata update()')
        extracted_metadata = media.extract_metadata(self.asset.path)
        print('extracted_metadata:')
        print(extracted_metadata)

        self.content = json.dumps(extracted_metadata)
        self.md5 = md5.getmd5(self.content)
        print(self.md5)

    def save(self, *args, **kwargs):
        print('metadata save()')

        # if self.content:
        #     print 'metadata has content'
        # else:
        #     print 'metadata no content: {}'.format(self.asset.path)
        #     self.content = json.dumps(media.extract_metadata(self.asset.path))
        #     # self.md5 = md5.getmd5(self.content)

        super(Metadata, self).save(*args, **kwargs)





@receiver(post_save, sender=Asset)
def create_metadata_for_new_assets(sender, instance, **kwargs):
        if instance.metadata:
            print 'has md'
            instance.metadata.save()
        else:
            print 'needs md'
            print instance
            print instance.path
            md = Metadata()
        #     md.content = json.dumps(media.extract_metadata(instance.path))
        # #     # self.md5 = md5.getmd5(self.content)
            md.save()
            instance.metadata = md
            instance.save()
            print 'done making md'

# # @receiver(pre_save, sender=Asset)
# def create_metadata_for_new_assets(sender, instance, **kwargs):
#     if instance.metadata:
#         print 'does not need more metadata'
#     else:
#         print 'needs moar metadata'



# @receiver(post_save, sender=Metadata)
# def import_metadata_on_create(sender, instance, **kwargs):
#     instance.update()
#     instance.save()