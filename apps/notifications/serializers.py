from rest_framework import serializers
from .models import Notification
from apps.accounts.serializers import UserProfileSerializer
from apps.posts.serializers import PostSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by_profile = serializers.SerializerMethodField()
    post_details = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = '__all__'

    def get_created_by_profile(self, obj):
        profile = obj.created_by.userprofile
        return UserProfileSerializer(profile).data

    def get_post_details(self, obj):
        if obj.post :
            return PostSerializer(obj.post).data
        else:
            return None
