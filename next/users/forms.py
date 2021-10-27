from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms
import requests
import socket 

# getting the user registered_ip_address
host_name = socket.gethostname()    
IPAddress = socket.gethostbyname(host_name)    
 

User = get_user_model()




class CustomSignupForm(forms.Form):
   
    first_name = forms.CharField(max_length=50, label='First Name')
 
    last_name = forms.CharField(max_length=30, label='Last Name')

    contact_number = forms.CharField(max_length=40, label='Contact Number')
 
    
 
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = _('Legal First & Middle Names')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Legal Last Names')
        self.fields['email'].widget.attrs['placeholder'] = _('Enter a valid Email Address')
        self.fields['contact_number'].widget.attrs['placeholder'] = _('Enter a valid Phone Number')
        # self.fields['country_of_residence'].label = False
        self.fields['email'].help_text = _('So we can send you confirmation of your registration')
        self.fields['first_name'].help_text = _('As show in your documents')
        self.fields['last_name'].help_text = _('As show in your documents')
        self.fields['contact_number'].help_text = _('So we can identify our customers incase of any emergency')
        # self.fields['account_type'].label = False
        # self.helper = FormHelper()
        # self.helper.form_show_labels = False
 
 
    def signup(self, request, user):
        group = Group.objects.get(name='customer')
        # client_ip, is_routable = get_client_ip(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.name = self.cleaned_data['first_name'] + " " + self.cleaned_data['last_name']
        user.contact_number = self.cleaned_data['contact_number']
        user.registered_ip_address = IPAddress
        user.groups.add(group)
        # user.agreed_to_data_usage = True
        # user.accept_terms = True
        # user.privacy_policy = True
        # user.gdpr_opt_out = True
        # user.is_business = True if self.cleaned_data['account_type'] == 'company' else False
        # user.is_personal = True if self.cleaned_data['account_type'] == 'individual' else False
        # user.default_currency = get_object_or_404(Currency, code=self.cleaned_data['country'].currency)
        # user.time_zone = time_zone()
        user.save()