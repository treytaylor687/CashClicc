from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'cashclicc.core'
    verbose_name = 'cc-core'

    def ready(self):
        import cashclicc.core.signals.handlers
        import cashclicc.core.signals.signals


