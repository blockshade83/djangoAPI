from rest_framework import serializers
from .models import *

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'about_user','contacts']

class StatusUpdateSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField('get_email')
    
    class Meta:
        model = StatusUpdate
        fields = ['email', 'posted_on', 'content']

    def get_email(self, obj):
        return AppUserSerializer(AppUser.objects.get(username=obj.author)).data['email']


class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField('get_from_details')
    to_user = serializers.SerializerMethodField('get_to_details')
    
    class Meta:
        model = ConnectionRequest
        fields = ['from_user', 'to_user', 'status']

    def get_from_details(self, obj):
        return AppUserSerializer(AppUser.objects.get(id=obj.initiated_by.id)).data

    def get_to_details(self, obj):
        return AppUserSerializer(AppUser.objects.get(id=obj.sent_to.id)).data