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
    file_path = models.TextField(null=True, blank=True, help_text='Displayable title', )
    file_path_md5 = models.CharField(null=True, blank=True, db_index=True, max_length=32, )
    preview = models.ImageField(null=True, blank=True, upload_to='previews/', height_field='preview_height', width_field='preview_width', max_length=256)
    preview_width = models.IntegerField(null=True, blank=True, db_index=True, )
    preview_height = models.IntegerField(null=True, blank=True, db_index=True, )
    md5 = models.CharField(null=True, blank=True, db_index=True, max_length=32, )

    class Meta:
        get_latest_by = 'datetime_updated'
        ordering = ['-datetime_updated', ]

    def __unicode__(self):
        if self.file_path:
            return u'%s' % (self.file_path)
        else:
            return u'(%s)' % (self.pk)

    def update_preview(self):
        path = self.file_path
        extension = misc.get_extension(path)

        if extension in settings.ENABLED_EXTENSIONS:
            preview_path_stub = os.path.join('previews/',self.file_path_md5 + '.jpg')
            print preview_path_stub
            preview_path = os.path.join(settings.MEDIA_ROOT,preview_path_stub)
            
            # previewing.delay(path, preview_path)

            print preview_path_stub
            self.preview=preview_path_stub

        print path
        return True

    def update_metadata(self):
        metadata, created = Metadata.objects.update_or_create(pk=self.pk)
        if created:
            print 'metadata created'
        else:
            print 'metadata updated'
        metadata.update()
        metadata.save()

    def save(self, *args, **kwargs):
        if self.file_path and not self.file_path_md5:
            self.file_path_md5 = md5.getmd5(self.file_path)

        if settings.PREVIEW_UPDATE_ON_SAVE:
            if self.file_path and not self.preview:
                self.update_preview()

        if settings.METADATA_UPDATE_ON_SAVE:
            if self.file_path:
                self.update_metadata()

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

        metadata_response = metadata(self.asset.file_path)
        if metadata_response:
            self.content = metadata_response
            print metadata_response
            self.md5 = md5.getmd5(metadata_response)
            return True
        else:
            return False

