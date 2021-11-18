from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.conf import settings


from .models import Cart, CartItem
from .views import _cart_id


User = settings.AUTH_USER_MODEL


@receiver(user_logged_in)
def add_cart_to_user(sender, request, **kwargs):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        is_cart_item_exist = CartItem.objects.filter(cart= cart).exists() #checking if the product and variation exists
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(cart=cart)

            # getting the product variation by cart id 
            p_variation = []
            for item in cart_item:
                variation = item.product_variation.all()
                p_variation.append(list(variation))

            # get the item from the user to access the product variations
            cart_item = CartItem.objects.filter(user = request.user)
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.product_variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)


            for pr in p_variation:
                if pr in ex_var_list:
                    index = ex_var_list.index(pr)
                    item_id = id[index]
                    item = CartItem.objects.get(id=item_id)
                    item.quantity += 1
                    item.user = request.user
                    item.save()
                else:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = request.user
                        item.save()
    except:
        print("not working")
