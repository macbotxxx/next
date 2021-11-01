from django.db import models
from django.db.models.fields import EmailField
from helpers.common.basemodel import BaseModel
from django.utils.translation import gettext_lazy as _


from next.users.models import User
from store.models import Product, ProductVariation


# Create your models here.

class Payement(BaseModel):
    """
    Payement model for accepting orders.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )

    payment_id = models.CharField(
        verbose_name = _("Payment ID"),
        max_length = 150,
        null=True,
        help_text=_("The payment identification number sent from the payment gateway.")
    )

    payment_method = models.CharField(
        verbose_name = _("Payment Method"),
        max_length = 150,
        null=True,
        help_text=_("The payment method used while paying for an order.")
    )

    amount_paid = models.CharField(
        verbose_name = _("Amount Paid"),
        max_length = 150,
        null=True,
        help_text=_("Amount paid for the above order by the customer.")
    )

    status = models.CharField(
        verbose_name = _("Payment Status"),
        max_length = 150,
        null=True,
        help_text=_("Payment status which identifies if the payment is set or not.")
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ('-created_date',)
        verbose_name = _("Payment")
        verbose_name_plural = _("Payment")

STATUS = (
    ('New', 'New'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)


class Order (BaseModel):
    """
    Order model which is consist of the customer order details 
    and payment status information.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )

    payment = models.ForeignKey(
        Payement, on_delete = models.CASCADE,
        null=True,blank=True,
        help_text=_("Customers order payment information.")
    )

    order_number = models.CharField(
        verbose_name = _("Order Number"),
        max_length = 150,
        null=True,
        help_text=_("Order generated number to identify the current customer order")
    )

    first_name = models.CharField(
        verbose_name = _("Legal First Name"),
        max_length = 150,
        null=True,
        help_text=_("Customer legal first name"),
    )

    last_name = models.CharField(
        verbose_name = _("Legal Last Name "),
        max_length = 150,
        null=True,
        help_text=_("Customer legal last name")
    )

    phone_number = models.CharField(
        verbose_name = _("Phone Number "),
        max_length = 150,
        null=True,
        help_text=_("Customers Phone Number")
    )

    email = models.EmailField(
        verbose_name = _("Customers Email"),
        max_length = 150,
        null=True,
        help_text=_("Customer email address for discount and notifications")
    )

    address_line_1  = models.CharField(
        verbose_name = _("Address Line 1"),
        max_length = 400,
        null=True,
        help_text=_("Customers address line 1 ")
    )

    address_line_2  = models.CharField(
        verbose_name = _("Address Line 2"),
        max_length = 400,
        null=True,blank=True,
        help_text=_("Customers address line 2 ")
    )

    state = models.CharField(
        verbose_name = _("Customers State"),
        max_length = 400,
        null=True,
        help_text=_("State of which the order is been placed from or to be shipped to.")
    )

    city = models.CharField(
        verbose_name = _("Order City"),
        max_length = 400,
        null=True,
        help_text=_("City of which the order is been placed from or to be shipped to.")
    )

    order_note = models.TextField(
        verbose_name = _("Order Note"),
        null=True,blank=True,
        help_text=_("A short note for the order to be delieved to you.")
    )

    shipping_rate_per_quantity = models.IntegerField(
        verbose_name = _("Order Shipping Rate"),
        null=True,blank=True,
        help_text=_("Shipping rate for the current order placed by the customer")
    )

    order_total = models.IntegerField(
        verbose_name = _("Order Total Amount"),
        null=True,blank=True,
        help_text=_("Total amount for the current order placed by the customer")
    )

    tax = models.IntegerField(
        verbose_name = _("Order Tax Amount"),
        null=True,blank=True,
        help_text=_("Tax amount for the current order placed by the customer")
    )

    status = models.CharField(
        choices=STATUS,default = 'New',
        verbose_name = _("Order Status"),
        max_length = 400,
        null=True,
        help_text=_("the current status of the order.")
    )

    ip_address = models.GenericIPAddressField(
        verbose_name = _("User Default IP Address"),
        max_length =60, 
        null=True,
        help_text = _("user default IP address hold the original ip address after registration, which a notification email will be sent to the user when a new ip address is been login to the account, and this is done for security reasons.")
    )

    is_ordered = models.BooleanField(
        verbose_name = _("Order Operation"),
        default=False,null=True,blank=True,
        help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
    )

    def __str__(self):
        return str(self.order_number)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("All Order")
        verbose_name_plural = _("All Order")


class OrderProduct (BaseModel):

    user = models.ForeignKey(
        User,
        verbose_name=_("User Profile"),
        on_delete=models.PROTECT, null=True,
        help_text=_("The user for whom account belongs to")
    )

    order = models.ForeignKey(
        Order, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the order table.")
        )

    payment = models.ForeignKey(
        Payement, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the payment table.")
        )

    product = models.ForeignKey(
        Product, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the product table.")
        )

    variation = models.ForeignKey(
        ProductVariation, on_delete = models.CASCADE,
        null=True, blank=True,
        help_text= _("foreign key and session to the product variation table.")
        )
    
    color = models.CharField(
        verbose_name = _("Product Color"),
        max_length = 400,
        null=True,
        help_text=_("product color for the current product variation.")
    )

    size = models.CharField(
        verbose_name = _("Product Size"),
        max_length = 400,
        null=True,
        help_text=_("product size for the current product variation.")
    )

    quantity = models.IntegerField(
        verbose_name = _("Product Quantity"),
        null = True, blank=True,
        help_text= _("product quantity for the current product been order by the customer.")
    )

    product_price = models.IntegerField(
        verbose_name = _("Product Price "),
        null=True,blank=True,
        help_text=_("price for the current product.")
    )

    ordered = models.BooleanField(
        verbose_name = _("Order Operation"),
        default=False,null=True,blank=True,
        help_text= _("the current state of the order , which identifies if the order is been processed successfully or not.")
    )

    
    def __str__(self):
        return str(self.user)

    class Meta:

        ordering = ('-created_date',)
        verbose_name = _("All Ordered Products")
        verbose_name_plural = _("All Ordered Products")
    
    

