from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import UserActivity, UserRegisteredIp

User = get_user_model()

from django.contrib.sessions.models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact_number')
    list_display_links = ('first_name', 'last_name', 'contact_number')
    readonly_fields = ('password',)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'hostname', 'ip_address')
    list_display_links = ('user', 'hostname', 'ip_address')


@admin.register(UserRegisteredIp)
class UserRegisteredIpAdin(admin.ModelAdmin):
    list_display = ('user', 'registered_ip_address')
    list_display_links = ('user', 'registered_ip_address')