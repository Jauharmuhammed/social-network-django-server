from rest_framework import serializers
from .models import Notification
from apps.accounts.serializers import UserProfileSerializer

class NotificationSerializer(serializers.ModelSerializer):
    created_by_profile = serializers.SerializerMethodField()
    class Meta:
        model = Notification
        fields = '__all__'

    def get_created_by_profile(self, obj):
        profile = obj.created_by.userprofile
        return UserProfileSerializer(profile).data
