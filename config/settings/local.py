from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "eL11HSttByEoHvSJazxndPml7bGrlQ63VDJgmv2N3eqsA5eRJmnX1AzEyhLCr4Tl",
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "165.227.197.121"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'support@nextcashandcarry.com.ng'
# EMAIL_HOST_PASSWORD = 'NexTSer@!!'
# EMAIL_PORT = '587'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# EMAIL_HOST = 'smtp.mailtrap.io'
# EMAIL_HOST_USER = 'f7f1d4d566645a'
# EMAIL_HOST_PASSWORD = '1917db4a003d90'
# EMAIL_PORT = '2525'

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405




# Your stuff...
# ------------------------------------------------------------------------------
# payments gateways private and public keys _______________________
# PAYSTACK_SECRET_KEY = env("PAY_STACK_SECRET_KEY")
# PAYSTACK_PUBLIC_KEY = env("PAY_STACK_PUBLIC_KEY")

FLUTTERWAVE_SECRET_KEY = "FLWSECK_TEST-c42542ddb1606364343282cca40553d6-X"
FLUTTERWAVE_PUBLIC_KEY = "FLWPUBK_TEST-f7d9f9de817c51ba37355d7a70b8224f-X"