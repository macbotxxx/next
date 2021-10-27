# Signals that fires when a user logs in and logs out
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from accounts.models import LoggedInUser
from next.users.models import UserActivity

# django email settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)




@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user')) 
    UserActivity.objects.create(user=kwargs.get('user'), hostname = hostname, ip_address = ip_address) 


@receiver(user_logged_in)
def checking_user_defualt_ip(sender, request, **kwargs):
    # getting the registered  user ip addresss
    registered_ip = request.user.registered_ip_address
    # getting the login user ip address
    logged_in_user_ip = ip_address

    """
    verifying both ip addresses and notify the user,
    if the login user is not a registered user or Ip address
    """

    if registered_ip is not logged_in_user_ip:
        # email template and context containing ipaddress and hostname
        subject = 'Securiy Warning - Next Cash and Carry Online Store'
        html_message = render_to_string(
            'emails/text.html',
            {
             'ipaddress': ip_address,
             'host': hostname,
            } 
        )
        plain_message = strip_tags(html_message)
        from_email = 'From <admin@next.com>'
        to = request.user.email
        mail.send_mail(subject, plain_message, from_email, [to], html_message = html_message)
    else:
        pass 


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
