from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Customer
from django.utils.translation import ugettext_lazy as _


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'last_login',)
    list_editable = ('is_active', 'user_type')
    list_filter = ('user_type', 'last_login')
    search_field = ('email', 'username',)
    list_display_links = ('email', 'username',)
    list_per_page = 25
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','phone','address','city','country',)}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       )
        }),
        (_('Important dates'), {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
admin.site.register(Customer)
admin.site.register(User,UserAdmin)

