from .models import Post, Tag, Comment, Collection
from rest_framework import serializers
from apps.accounts.serializers import UserProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(
        source='get_user_profile', read_only=True)
    comments_count = serializers.CharField(
        source='get_comments_count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'image', 'title', 'user', 'tags', 'description',
                  'location', 'created', 'user_profile', 'comments_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='get_user_name', read_only=True)
    profile_pic = serializers.URLField(
        source='get_user_profile_pic', read_only=True)
    replies_count = serializers.CharField(
        source='get_replies_count', read_only=True)
    likes_count = serializers.CharField(
        source='get_likes_count', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    profile_pic = serializers.URLField( source='get_user_profile_pic', read_only=True)
    cover = serializers.SerializerMethodField()
    class Meta:
        model = Collection
        fields = [ 'id', 'name', 'slug', 'user', 'posts', 'cover', 'collaborators', 'created', 'updated', 'active', 'private', 'profile_pic']

    def get_cover(self, obj):
        if obj.cover:
            return obj.cover.url
        else:
            return None