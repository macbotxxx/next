from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address_line_1', 'address_line_2','state', 'city', 'order_note',]

        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop("request")
        #     super(OrderForm, self).__init__(*args, **kwargs)
        #     self.fields['first_name'].initial = self.request.user.first_name
        #     self.fields['last_name'].initial = self.request.user.last_name
            # self.fields['phone_number'].initial = self.request.user.phone_number