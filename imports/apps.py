from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class ImportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "imports"

    def ready(self):
        # BÜTÜN yüklü app’lerin içinde varsa `<app>.importers` modülünü import et
        # Böylece @register(...) çağrıları çalışır ve registry dolar.
        autodiscover_modules("importers")

