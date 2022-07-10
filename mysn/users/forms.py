from django import forms
from users.models import AppUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True, label = 'Email')
    first_name = forms.CharField(required = True, label = 'First Name', max_length = 50)
    last_name = forms.CharField(required = True, label = 'Last Name', max_length = 100)
    country = forms.CharField(required = True, label = 'Country', max_length = 100)
    about_user = forms.CharField(required = False, label = 'Add some information about you', max_length = 1000)

    def clean(self):
        super(UserCreationForm, self).clean()

        if self.cleaned_data.get('email') == '':
            raise ValidationError('Email field is mandatory')

        if self.cleaned_data.get('first_name') == '':
            raise ValidationError('First Name field is mandatory')

        if self.cleaned_data.get('last_name') == '':
            raise ValidationError('Last Name field is mandatory')

        if self.cleaned_data.get('country') == '':
            raise ValidationError('Country field is mandatory')

    class Meta:
        model = AppUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'country', 'about_user')


class UpdateForm(UserChangeForm):
    first_name = forms.CharField(required = True, label = 'First Name', max_length = 50)
    last_name = forms.CharField(required = True, label = 'Last Name', max_length = 100)
    country = forms.CharField(required = True, label = 'Country', max_length = 100)
    about_user = forms.CharField(required = False, label = 'Add some information about you', max_length = 1000)

    def clean(self):
        super(UserChangeForm, self).clean()

        if self.cleaned_data.get('first_name') == '':
            raise ValidationError('First Name field is mandatory')

        if self.cleaned_data.get('last_name') == '':
            raise ValidationError('Last Name field is mandatory')
        
        if self.cleaned_data.get('country') == '':
            raise ValidationError('Country field is mandatory')

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'country', 'about_user')