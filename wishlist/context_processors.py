from .models import Wishlist


def wishlist_counter(request):
    wish_count = Wishlist.objects.filter(user=request.user).count()
    return dict(wish_count=wish_count)

