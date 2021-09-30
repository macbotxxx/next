from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import UserActivity

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number')
    list_display_links = ('first_name', 'last_name', 'contact_number')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostname', 'ip_address')
    list_display_links = ('user', 'hostname', 'ip_address')
