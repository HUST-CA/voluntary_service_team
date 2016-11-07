from django.apps import AppConfig


class ServiceInformConfig(AppConfig):
    name = 'service_inform'

    def ready(self):
        from . import signals