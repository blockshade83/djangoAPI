from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm, UpdateForm
from .models import *

# fields = list(UserAdmin.fieldsets)
# fields[0] = (None, {'fields': ('username', 'password', 'is_bot_flag')})
# UserAdmin.fieldsets = tuple(fields)

class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = UpdateForm
    model = AppUser
    list_display = ('email', 'is_staff', 'is_active','first_name','last_name')
    list_filter = ('email', 'is_staff', 'is_active','first_name','last_name')
    fieldsets = (
        (None, {'fields': ('password','first_name','last_name','country','about_user')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','first_name','last_name','country','about_user')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(AppUser, CustomUserAdmin)