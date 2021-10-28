from django.apps import AppConfig


class CartsConfig(AppConfig):
    name = 'carts'

    # This function is the only new thing in this file
    # it just imports the signal file when the app is ready
    def ready(self):
        import carts.signals
