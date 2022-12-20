from .models import Post, Tag
from rest_framework import serializers
from apps.accounts.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(source='get_user_profile', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'user', 'description', 'created', 'user_profile']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'