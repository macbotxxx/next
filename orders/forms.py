from django import forms
from next.users.models import Shipping_Address


# class OrderForm(forms.ModelForm):
    
#     class Meta:
#         model = Shipping_Address
#         fields = ['first_name', 'last_name', 'phone_number', 'email', 'address_line_1', 'address_line_2','state', 'city', ]

#         # def __init__(self, *args, **kwargs):
#         #     self.request = kwargs.pop("request")
#         #     super(OrderForm, self).__init__(*args, **kwargs)
#         #     self.fields['first_name'].initial = self.request.user.first_name
#         #     self.fields['last_name'].initial = self.request.user.last_name
#             # self.fields['phone_number'].initial = self.request.user.phone_number
            

STATES = (
        ('','Select States'),
        #   ("Abia","Abia"),
        #   ("Adamawa","Adamawa"),
        #   ("Akwa Ibom","Akwa Ibom"),
        #   ("Anambra","Anambra"),
        #   ("Bauchi","Bauchi"),
        #   ("Bayelsa","Bayelsa"),
        #   ("Benue","Benue"),
        #   ("Borno","Borno"),
        #   ("Cross River","Cross River"),
        #   ("Delta","Delta"),
        #   ("Ebonyi","Ebonyi"),
        #   ("Edo","Edo"),
        #   ("Ekiti","Ekiti"),
        #  ( "Enugu","Enugu"),
        ("FCT - Abuja","FCT - Abuja"),
        #  ( "Gombe","Gombe"),
        #  ( "Imo","Imo"),
        #  ( "Jigawa","Jigawa"),
        #  ( "Kaduna","Kaduna"),
        #  ( "Kano","Kano"),
        #  ( "Katsina","Katsina"),
        #  ( "Kebbi","Kebbi"),
        #  ( "Kogi","Kogi"),
        #  ( "Kwara","Kwara"),
        #  ( "Lagos","Lagos"),
        #  ( "Nasarawa","Nasarawa"),
        #  ( "Niger","Niger"),
        #  ( "Ogun","Ogun"),
        # (  "Ondo","Ondo"),
        #  ( "Osun","Osun"),
        #  ( "Oyo","Oyo"),
        #  ( "Plateau","Plateau"),
        (  "Rivers","Rivers"),
        #  ( "Sokoto","Sokoto"),
        #  ( "Taraba","Taraba"),
        #  ( "Yobe","Yobe"),
        #  ( "Zamfara","Zamfara"),
        
        )

PAYMENT_CHOICES = (
      ('Paid Online', 'Pay Online'),
      ('Pay On Delivery', 'Pay On Delivery'),
      ('Paid From Wallet', 'Pay From Wallet'),
)

class OrderForm(forms.Form):
      first_name = forms.CharField(required=False)
      last_name = forms.CharField(required=False)
      phone_number = forms.CharField(required=False)
      email = forms.EmailField(required=False)
      address_line_1 = forms.CharField(required=False)
      address_line_2 = forms.CharField(required=False)
      shipping_local_gov = forms.CharField(required=False)
      shipping_state = forms.ChoiceField(widget=forms.Select(attrs={'class':'single-select2'}), choices=STATES, required=False)
      widget=forms.TextInput(attrs={'class':'form-control'})

      # same_billing_address = forms.BooleanField(required=False)
      set_default_shipping = forms.BooleanField(required=False)
      use_default_shipping = forms.BooleanField(required=False)
   

    #   payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
