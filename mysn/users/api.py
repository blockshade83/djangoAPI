from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from .models import *
from .serializers import *

# path /api/users
@api_view(['GET'])
@csrf_exempt
def get_users(request):
    users = AppUser.objects.all()
    if request.method == 'GET':
        serializer = AppUserSerializer(users, many=True)
        return Response(serializer.data)

# path /api/user_posts/<username>
@api_view(['GET'])
@csrf_exempt
def get_user_posts(request, username):
    try:
        user_id = AppUser.objects.get(username=username)
    except AppUser.DoesNotExist:
        return HttpResponse(status=404)
    
    # get user posts for username
    user_posts = StatusUpdate.objects.filter(author=user_id.id)
    if request.method == 'GET':
        serializer = StatusUpdateSerializer(user_posts, many=True)
        return Response(serializer.data)

# path /api/user_contacts/<username>
@api_view(['GET'])
@csrf_exempt
def get_user_contacts(request, username):
    try:
        user_id = AppUser.objects.get(username=username)
    except AppUser.DoesNotExist:
        return HttpResponse(status=404)
    
    # get user contacts for username
    if request.method == 'GET':
        contacts = AppUserSerializer(user_id).data['contacts']
        contact_instances = AppUser.objects.filter(id__in=contacts)
        serializer = AppUserSerializer(contact_instances, many=True)
        return Response(serializer.data)

# path api/pending_connection_requests/
@api_view(['GET'])
@csrf_exempt
def pending_connection_requests(request):
    # get connection records in status pending
    connections = ConnectionRequest.objects.filter(status="pending")
    # serialize connection records
    serializer = ConnectionRequestSerializer(connections, many=True)
    return Response(serializer.data)