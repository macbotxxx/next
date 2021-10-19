import random
import string
from django.utils.text import slugify


#  creating slugs starts from here 

def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.product_name)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=6)
            )
            return unique_slug_generator(instance,new_slug=new_slug)
      return slug

 

def unique_slug_generator_category(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.category)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=4)
            )
            return unique_slug_generator_category(instance,new_slug=new_slug)
      return slug



def unique_slug_generator_brand(instance, new_slug=None):
      if new_slug is not None:
            slug = new_slug
      else:
            slug = slugify(instance.brand)

      klass = instance.__class__
      qs_exists = klass.objects.filter(slug=slug).exists()
      if qs_exists:
            new_slug="{slug}-{randstr}".format(
                  slug=slug,
                  randstr = random_string_generator(size=4)
            )
            return unique_slug_generator_brand(instance,new_slug=new_slug)
      return slug



# Wallet ID generator based on registered users

def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_wallet_id_generator(instance):
    order_new_id= random_string_generator()
    Klass= instance.__class__
    qs_exists= Klass.objects.filter(wallet_id= order_new_id).exists()
    if qs_exists:
        return unique_wallet_id_generator(instance)
    return order_new_id
