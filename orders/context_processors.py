from django.conf import settings

def secret_key(request):
    key = settings.FLUTTERWAVE_PUBLIC_KEY
    return dict(key=key)

