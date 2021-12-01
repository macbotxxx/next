from store.models import Brands

def all_brand (request):
    all_brands = Brands.objects.all()
    return dict(all_brands=all_brands)
