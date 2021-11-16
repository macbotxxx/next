from django import forms
from django.utils.translation import gettext_lazy as _

class ProfileSettingsForm(forms.Form):
    first_name = forms.CharField(
        # verbose_name = _('Your Legal First Name'),
        max_length =50,
        help_text=_("Your legal first name, which will be used as default name when checking out an order."),
    )

    last_name = forms.CharField(
        # verbose_name = _('Your Legal Last Name'),
        max_length =50,
        help_text=_("Your legal last name, which will be used as default name when checking out an order."),
    )

    phone_number = forms.CharField(
        # verbose_name = _('Phone Number'),
        max_length =12,
        help_text=_("input your phone number"),
    )



