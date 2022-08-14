from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
from .forms import *
from .serializers import *
import os

# function to return the contacts of the user
def get_user_context(user, userid):
    user_instance = AppUser.objects.get(id=userid)
    serializer = AppUserSerializer(user_instance)
    contacts = serializer.data['contacts']
    contacts_list = []
    for result in contacts:
        contact = AppUser.objects.get(id=result)
        contacts_list.append(contact)

    incoming_connections = ConnectionRequest.objects.filter(Q(sent_to=user) & Q(status='pending')).count()
    outgoing_connections = ConnectionRequest.objects.filter(Q(initiated_by=user) & Q(status='pending')).count()

    return {'incoming_connections': incoming_connections,
            'outgoing_connections': outgoing_connections,
            'contacts_list': contacts_list}

def index(request):
    if request.user.is_authenticated:
        status_update_form = StatusUpdateForm()
        
        status_update_history = StatusUpdate.objects.filter(author=request.user).order_by('-posted_on')
        status_update_list = []
        for element in status_update_history:
            status_update_list.append(element)

        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)

        return render(request, 'index.html', {'status_update_form': status_update_form, 
                                              'status_update_list': status_update_list,
                                              'incoming_connections': context['incoming_connections'],
                                              'outgoing_connections': context['outgoing_connections'],
                                              'contacts': context['contacts_list']})
    else:
        return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(data = request.POST)
        if user_form.is_valid():
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

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def status_update(request):
    if request.method == 'POST':
        status_update_form = StatusUpdateForm(data = request.POST)
        if status_update_form.is_valid():
            cleaned_data = status_update_form.cleaned_data
            # print(cleaned_data)
            status_update_record = StatusUpdate(author = request.user, content = cleaned_data['content'])
            status_update_record.save()
            return HttpResponseRedirect('/')
    else:
        # status_update_form = StatusUpdateForm()
        return HttpResponse("Invalid request")

@login_required
def search(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
        search_text_list = search_text.split()
        results_list = []
        for word in search_text_list:
            results = AppUser.objects.filter(Q(username__icontains=word) | Q(first_name__icontains=word) | Q(last_name__icontains=word))
            for result in results:
                if result not in results_list:
                    results_list.append(result)
        # get pending connections and user contacts for the left section of the page            
        context = get_user_context(request.user, request.user.id)
        return render(request, 'search_results.html', {'results_list': results_list, 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def get_user_instance(user_id):
    print('get_user_instance function called')
    try:
        user_id_record = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        return HttpResponse(status=404)
    return user_id_record

@login_required
@csrf_exempt
def get_profile(request, user_id):
    try:
        user_id_record = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        return HttpResponse(status=404)

    outgoing_connection_status = ""
    incoming_connection_status = ""
    current_contact = False

    outgoing_connections = ConnectionRequest.objects.filter(Q(initiated_by_id=request.user.id) & Q(sent_to_id=user_id_record.id))
    incoming_connections = ConnectionRequest.objects.filter(Q(initiated_by_id=user_id_record.id) & Q(sent_to_id=request.user.id))

    for record in outgoing_connections:
        if record.status == 'pending':
            outgoing_connection_status = 'pending'

    for record in incoming_connections:
        if record.status == 'pending':
            incoming_connection_status = 'pending'

    user_instance = AppUser.objects.get(id=request.user.id)
    serializer = AppUserSerializer(user_instance)
    contacts = serializer.data['contacts']

    if user_id_record.id in contacts:
        current_contact = True

    if request.method == 'GET':
        status_update_history = StatusUpdate.objects.filter(author=user_id_record.id).order_by('-posted_on')
        status_update_list = []
        for element in status_update_history:
            status_update_list.append(element)
        
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)

        return render(request, 'profile.html', {'profile':user_id_record, 
                                                'status_update_list': status_update_list, 
                                                'outgoing_connection_status': outgoing_connection_status, 
                                                'incoming_connection_status': incoming_connection_status,
                                                'incoming_connections': context['incoming_connections'],
                                                'outgoing_connections': context['outgoing_connections'],
                                                'current_contact': current_contact ,
                                                'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def connect_initiate(request):
    if request.method == 'POST':
        initiated_by_instance = AppUser.objects.get(id=request.POST['initiated_by'])
        sent_to_instance = AppUser.objects.get(id=request.POST['sent_to']) 
        connection_record = ConnectionRequest(initiated_by = initiated_by_instance, sent_to = sent_to_instance)
        connection_record.save()
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'request_result.html', {'text': 'Connection Request sent', 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def connect_accept(request):
    if request.method == 'POST':
        # get instance objects for logged in user and profile user
        initiated_by_instance = AppUser.objects.get(id=request.POST['initiated_by'])
        sent_to_instance = AppUser.objects.get(id=request.POST['sent_to'])
        # mark the pending connection requests from the profile user as completed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=initiated_by_instance) & Q(sent_to=sent_to_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'completed'
                connection.save()
        # mark the pending outgoing connection request to the profile user as completed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=sent_to_instance) & Q(sent_to=initiated_by_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'completed'
                connection.save()
        # add profile user as a contact of the logged in user
        initiated_by_instance.contacts.add(sent_to_instance)
        # add logged in user as a contact of the profile user
        sent_to_instance.contacts.add(initiated_by_instance)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'request_result.html', {'text': 'Connection Request accepted', 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def connect_reject(request):
    if request.method == 'POST':
        # get instance objects for logged in user and profile user
        initiated_by_instance = AppUser.objects.get(id=request.POST['initiated_by'])
        sent_to_instance = AppUser.objects.get(id=request.POST['sent_to'])
        # mark the pending connection requests from the profile user as closed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=initiated_by_instance) & Q(sent_to=sent_to_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'closed'
                connection.save()
        # mark the pending outgoing connection request to the profile user as closed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=sent_to_instance) & Q(sent_to=initiated_by_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'closed'
                connection.save()
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)

        return render(request, 'request_result.html', {'text': 'Connection Request rejected', 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def connect_withdraw(request):
    if request.method == 'POST':
        # get instance objects for logged in user and profile user
        initiated_by_instance = AppUser.objects.get(id=request.POST['initiated_by'])
        sent_to_instance = AppUser.objects.get(id=request.POST['sent_to'])
        # mark the pending connection requests from the profile user as closed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=initiated_by_instance) & Q(sent_to=sent_to_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'closed'
                connection.save()
        # mark the pending outgoing connection request to the profile user as closed
        connection_requests = ConnectionRequest.objects.filter(Q(initiated_by=sent_to_instance) & Q(sent_to=initiated_by_instance))
        for connection in connection_requests:
            if connection.status == 'pending':
                connection.status = 'closed'
                connection.save()
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'request_result.html', {'text': 'Connection Request withdrawn', 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def current_contacts(request):
    if request.method == 'GET':
        user_instance = AppUser.objects.get(id=request.user.id)
        serializer = AppUserSerializer(user_instance)
        contacts = serializer.data['contacts']
        results_list = []
        for result in contacts:
            contact = AppUser.objects.get(id=result)
            results_list.append(contact)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'search_results.html', {'results_list': results_list, 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def incoming_connection_requests(request):
    if request.method == 'GET':
        results = ConnectionRequest.objects.filter(Q(sent_to=request.user) & Q(status='pending'))
        results_list = []
        for result in results:
            results_list.append(result.initiated_by)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'search_results.html', {'results_list': results_list, 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def outgoing_connection_requests(request):
    if request.method == 'GET':
        results = ConnectionRequest.objects.filter(Q(initiated_by=request.user) & Q(status='pending'))
        results_list = []
        for result in results:
            results_list.append(result.sent_to)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'search_results.html', {'results_list': results_list, 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateForm(request.POST, request.FILES)
        
        if user_form.is_valid():
            user_instance = AppUser.objects.get(id=request.user.id)
            user_instance.first_name = user_form.cleaned_data.get('first_name')
            user_instance.last_name = user_form.cleaned_data.get('last_name')
            user_instance.country = user_form.cleaned_data.get('country')
            user_instance.about_user = user_form.cleaned_data.get('about_user')

            if len(request.FILES) > 0:
                user_instance.photo = request.FILES['photo']
                try:
                    # remove current profile photo, if it exists
                    os.remove(user_instance.photo.path)
                except Exception as error:
                    print(error)

            user_instance.save()
            return HttpResponseRedirect('/')

    else:
        data = {'first_name': request.user.first_name, 
                'last_name': request.user.last_name,
                'country': request.user.country,
                'about_user': request.user.about_user}
        user_form = UpdateForm(data)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'update_profile.html', {'user_form': user_form, 
                                                       'incoming_connections': context['incoming_connections'],
                                                       'outgoing_connections': context['outgoing_connections'],
                                                       'contacts': context['contacts_list']})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        upload_form = PhotoUploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            photo_record = UserPhoto(owner = request.user, photo = request.FILES['photo'])
            photo_record.save()
            return HttpResponseRedirect('gallery')
        else:
            return HttpResponse("Invalid submission")
    else:
        upload_form = PhotoUploadForm()
        return HttpResponse("Invalid request")

@login_required
def gallery(request):
    if request.method == 'GET':
        user_photos = UserPhoto.objects.filter(owner=request.user).order_by('-added_on')
        user_photos_list = []
        for record in user_photos:
            user_photos_list.append(record.photo)
        upload_form = PhotoUploadForm()
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'gallery.html', {'photos': user_photos_list, 
                                                'upload_form': upload_form, 
                                                'photos_user': request.user, 
                                                'incoming_connections': context['incoming_connections'],
                                                'outgoing_connections': context['outgoing_connections'],
                                                'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")

@login_required
def get_gallery(request, user_id):
    try:
        user_id_record = AppUser.objects.get(id=user_id)
    except AppUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        user_photos = UserPhoto.objects.filter(owner=user_id_record.id).order_by('-added_on')
        user_photos_list = []
        for record in user_photos:
            user_photos_list.append(record.photo)
        # get pending connections and user contacts for the left section of the page
        context = get_user_context(request.user, request.user.id)
        return render(request, 'gallery.html', {'photos': user_photos_list, 
                                                'photos_user': user_id_record, 
                                                'incoming_connections': context['incoming_connections'],
                                                'outgoing_connections': context['outgoing_connections'],
                                                'contacts': context['contacts_list']})
    else:
        return HttpResponse("Invalid request")