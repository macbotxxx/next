from .models import Wishlist


def wishlist_counter(request):
    if request.user.is_authenticated():
        wish_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wish_count = 0
    return dict(wish_count=wish_count)

