from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'AroundLB Core Application'

    def ready(self):
        import core.signals