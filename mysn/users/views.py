from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *

def index(request):
    return render(request, 'index.html')

def register(request):

    if request.method == 'POST':
        user_form = RegistrationForm(data = request.POST)
        if user_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            email = user_form.cleaned_data.get('email')
            messages.success(request, f'Account was succesfully created for {email}. Please login to continue')
            return redirect('/')

    else:
        user_form = RegistrationForm()
        return render(request, 'registration.html', {'user_form': user_form})