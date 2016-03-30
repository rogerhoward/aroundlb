from __future__ import unicode_literals

import uuid
import os
import simplejson as json

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.conf import settings

# import core.tools.media as media
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
    type = models.CharField(null=True, blank=True, db_index=True, max_length=32, )

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
    original = models.ImageField(null=True, blank=True, upload_to='originals/', height_field='original_height', width_field='original_width')
    original_width = models.IntegerField(null=True, blank=True, db_index=True, )
    original_height = models.IntegerField(null=True, blank=True, db_index=True, )
    md5 = models.CharField(null=True, blank=True, db_index=True, max_length=32, )

    class Meta:
        get_latest_by = 'datetime_updated'
        ordering = ['-datetime_updated', ]

    def __unicode__(self):
        if self.original:
            return u'%s' % (self.original.url)
        else:
            return u'(%s)' % (self.pk)

    def path(self):
        if self.original:
            return os.path.join(settings.MEDIA_ROOT, self.original.url)
        else:
            return False

    def update_metadata(self):
        metadata, created = Metadata.objects.update_or_create(pk=self.pk)
        if created:
            print 'metadata created'
        else:
            print 'metadata updated'
        metadata.update()
        metadata.save()

    def save(self, *args, **kwargs):
        print self.path()

        if self.original and not self.md5:
            self.md5 = md5.getmd5(self.path())


        super(Asset, self).save(*args, **kwargs)


class Round(Asset):
    """
    Represents unique Rounds.
    """
    title = models.TextField(null=True, blank=True, help_text='Displayable title', )
    name = models.CharField(null=True, blank=True, db_index=True, max_length=256, )


class Metadata(GenericBaseClass):
    """
    Represents unique Metadata.
    """
    asset = models.OneToOneField('Asset', 
                                related_name='metadata', 
                                db_index=True , 
                                primary_key=True, )
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

        metadata_response = metadata(self.asset.path())
        if metadata_response:
            self.content = metadata_response
            print metadata_response
            self.md5 = md5.getmd5(metadata_response)
            return True
        else:
            return False

