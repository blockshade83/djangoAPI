from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def index(request):
    if request.user.is_authenticated:
        status_update_form = StatusUpdateForm()
        
        status_update_history = StatusUpdate.objects.filter(author=request.user).order_by('-posted_on')
        status_update_list = []
        for element in status_update_history:
            status_update_list.append(element)

        return render(request, 'index.html', {'status_update_form': status_update_form, 'status_update_list': status_update_list})
    else:
        return render(request, 'index.html')

def register(request):

    if request.method == 'POST':
        user_form = RegistrationForm(data = request.POST)
        if user_form.is_valid:
            user_form.save()
            email = user_form.cleaned_data.get('email')
            return render(request, 'registration/login.html', {'new_account': True})

    else:
        user_form = RegistrationForm()
        return render(request, 'registration/register.html', {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            return render(request, 'registration/login.html', {'error': True})

    else:
        return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def status_update(request):
    if request.method == 'POST':
        status_update_form = StatusUpdateForm(data = request.POST)
        if status_update_form.is_valid():
            cleaned_data = status_update_form.cleaned_data
            print(cleaned_data)
            status_update_post = StatusUpdate(author = request.user, content = cleaned_data['content'])
            status_update_post.save()
            return HttpResponseRedirect('/')
    else:
        status_update_form = StatusUpdateForm()
        return render(request, 'index.html', {'status_update_form': status_update_form})