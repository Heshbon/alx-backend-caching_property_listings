from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    name = 'properties'
    verbose_name = "Properties"

    def ready(self):
        """Import signals when the app is ready"""
        import properties.signals