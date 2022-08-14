from rest_framework import serializers
from .models import *

# serializer for user instances
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'about_user','contacts']

# serializer for status updates
class StatusUpdateSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField('get_email')
    
    class Meta:
        model = StatusUpdate
        fields = ['email', 'posted_on', 'content']

    def get_email(self, obj):
        return AppUserSerializer(AppUser.objects.get(username=obj.author)).data['email']

# serializer for connection requests
class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField('get_from_details')
    to_user = serializers.SerializerMethodField('get_to_details')
    
    class Meta:
        model = ConnectionRequest
        fields = ['from_user', 'to_user', 'status']

    # get user instance for initiating user
    def get_from_details(self, obj):
        return AppUserSerializer(AppUser.objects.get(id=obj.initiated_by.id)).data
    # get user instance for receiving user
    def get_to_details(self, obj):
        return AppUserSerializer(AppUser.objects.get(id=obj.sent_to.id)).data