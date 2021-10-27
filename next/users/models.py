from helpers.common.basemodel import BaseModel
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField #Bug to be fix -- target=  trying to have a phone number field 

import uuid



class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The given email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)



class User(AbstractUser):
    """Default user for investodd."""
    objects = UserManager()

    KYC_STATUS = (
        ('unverified', _('Unverified')),
        ('pending', _('Pending')),
        ('verified', _('Verified')),
        ('action_required', _('Action_required')),
        ('cancelled', _('Cancelled')),
        ('rejected', _('Rejected/Refused'))
    )


    id = models.UUIDField(
        default = uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text=_("The unique identifier of the investor.")
    )

     #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)

    email = models.EmailField(
        max_length=150,
        null=True,
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("The email address of the investor.")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    username = None


    first_name = models.CharField(
        verbose_name=_("First names"),
        max_length=50,
        null=True,
        help_text=_("The first nammes of the investor.")
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name=_("Last names"),
        null=True,
        help_text=_("The last nammes of the investor.")
    )

    contact_number = models.CharField(
        max_length=50,
        verbose_name=_("Last names"),
        null=True,
        help_text=_("The last nammes of the investor.")
    )
    phone = PhoneNumberField(null=True, blank=False, unique=True)

    default_currency_id = models.CharField(
        max_length=3,
        verbose_name=_("Default Currency ID"),
        blank=True, null=True,
        default='NGN',
        help_text=_("The default currency of the investor. Currency will be sent against Customer country of residence.")
    )

    registered_ip_address = models.GenericIPAddressField(
        verbose_name = _("User Default IP Address"),
        max_length =60, 
        null=True,
        help_text = _("user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.")
    )

    class Meta:
        verbose_name = _("All Registered Customer")
        verbose_name_plural = _("All Registered Customer")

    def __str__(self):
        return str(self.email)


    def get_absolute_url(self):
        """
        Get url for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.pk})


@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_user_registed_ip(sender, instance, created, **kwargs):
    if created:
        UserRegisteredIp.objects.create(user=instance,registered_ip_address = instance.registered_ip_address, is_active = True)
        print('profile is created')

class UserRegisteredIp (BaseModel):
    """
    registering user ip address 
    """
    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )

    registered_ip_address = models.GenericIPAddressField(
        verbose_name = _("User Default IP Address"),
        max_length =60, 
        null=True,
        help_text = _("user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.")
    )

    is_active = models.BooleanField(
        verbose_name = _("IP Address Status"),
        default = False,
        null=True,
        help_text = _("The user ip address status which is to be set for accepting user ip address ")
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("users Registered IP Address")
        verbose_name_plural = _("users Registered IP Address")

    def __str__(self):
        return str(self.user)




class UserActivity (BaseModel):
    """ 
    An Activity Log (also known as an Activity Diary is a written record of how a user spend time. 
    you can then change the way that you work to eliminate them.
    """

    user = models.ForeignKey(
        'User',
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT,
        help_text=_("The user for whom account belongs to")
    )

    hostname = models.CharField(
        verbose_name=_("Host Name"),
        max_length=355,
        null=True,blank=True,
        help_text=_("The Host Name of the logged in user system")
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("System IP Address"),
        null=True, blank=True, 
        editable=False,
        help_text=_(" The system IP address to current login user")
    )

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("All Users Activity")
        verbose_name_plural = _("All Users Activity")

    def __str__(self):
        return str(self.user)
