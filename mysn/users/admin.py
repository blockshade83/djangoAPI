from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegistrationForm, UpdateForm
from .models import *

# customize UserAdmin class
class CustomUserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = UpdateForm
    model = AppUser
    list_display = ('username','email', 'is_staff', 'is_active','first_name','last_name')
    list_filter = ('email', 'is_staff', 'is_active','first_name','last_name')
    fieldsets = (
        (None, {'fields': ('email','password','first_name','last_name','country','about_user','contacts')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', 'is_staff', 'is_active','first_name','last_name','country','about_user','contacts')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# register models to admin site
admin.site.register(AppUser, CustomUserAdmin)
admin.site.register(StatusUpdate)
admin.site.register(ConnectionRequest)