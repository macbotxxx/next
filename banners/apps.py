from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BannersConfig(AppConfig):
    name = 'banners'
    verbose_name = _(" Banners and Ad Images")
