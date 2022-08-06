from django import forms
from users.models import AppUser, StatusUpdate, UserPhoto
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings

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
        fields = ('username', 'email', 'first_name', 'last_name', 'country', 'about_user')


class UpdateForm(UserChangeForm):
    first_name = forms.CharField(required = True, label = 'First Name', max_length = 50)
    last_name = forms.CharField(required = True, label = 'Last Name', max_length = 100)
    country = forms.CharField(required = True, label = 'Country', max_length = 100)
    about_user = forms.CharField(required = False, label = 'Add some information about you')
    photo = forms.ImageField(required = False)

    password = None

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
        fields = ('first_name', 'last_name', 'country', 'about_user','photo')

class StatusUpdateForm(forms.Form):
    author = 'Author'
    content = forms.CharField(required = True, label = '', widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':50}))

    def clean(self):
        super(forms.Form, self).clean()

        if self.cleaned_data.get('content') == '':
            raise ValidationError('Status update cannot be empty')

    class Meta:
        model = StatusUpdate
        fields = ['author', 'content']

# class ConnectionForm(forms.Form):
#     # initiated_by = forms.CharField(required = True)
#     # sent_to = forms.CharField(required = True)

#     def clean(self):
#         super(forms.Form, self).clean()

#         if self.cleaned_data.get('initiated_by') == '':
#             raise ValidationError('User cannot be empty')

#         if self.cleaned_data.get('sent_to') == '':
#             raise ValidationError('User to connect to cannot be empty')
        
#     class Meta:
#         model = AppUser
#         fields = ['initiated_by', 'sent_to']

class PhotoUploadForm(forms.Form):
    owner = 'Owner'
    photo = forms.ImageField(required = True)

    class Meta:
        model = UserPhoto
        fields = ['owner', 'photo']
