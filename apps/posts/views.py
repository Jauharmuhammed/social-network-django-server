from django.shortcuts import render

from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes, APIView
from rest_framework.response import Response

from .models import Post, Tag, Comment, Collection
from .serializers import PostSerializer, TagSerializer, CommentSerializer, CollectionSerializer
from apps.accounts.models import CustomUser

from django.db.models.functions import Now
from django.db import IntegrityError

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    image = request.data['image']
    title = request.data['title']
    description = request.data['description']
    location = request.data['location']

    tags = request.data['tags'].split(',')

    post = Post.objects.create(
        user=user,
        image=image,
        title=title,
        description=description,
        location=location,
    )

    if tags is not None:
        for tag in tags:
            if tag.strip() == '':
                continue

            tag_instance = Tag.objects.filter(name__iexact=tag).first()
            if not tag_instance:
                tag_instance = Tag.objects.create(name=tag.lower())
            post.tags.add(tag_instance)
    post.save()

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_post(request, id):
    print(request.data)
    title = request.data['title']
    description = request.data['description']
    location = request.data['location']

    tags = request.data['tags'].split(',')

    post = Post.objects.get(id=id)
    post.title = title
    post.description = description
    post.location = location

    print(post.tags.all())

    for tag in list(post.tags.all()):
        print(tag)
        if tag not in tags:
            print(tag)
            print(tags)

            post.tags.remove(tag)

    if tags is not None:
        for tag in tags:
            if tag.strip() == '':
                continue
            if tag not in list(post.tags.all()):
                tag_instance = Tag.objects.filter(name__iexact=tag).first()
                if not tag_instance:
                    tag_instance = Tag.objects.create(name=tag.lower())
                post.tags.add(tag_instance)

    post.save()

    post.save()

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_by_post(request, id):
    comments = Comment.objects.filter(
        post=id, parent=None).order_by('-created')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_replies(request, id):
    comments = Comment.objects.filter(parent=id).order_by('created')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    posts = tag.posts.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, id):
    user = request.user
    try:
        comment_to_like = Comment.objects.get(id=id)
        print(comment_to_like)
        if user in comment_to_like.like.all():
            comment_to_like.like.remove(user)
            comment_to_like.save()
            return Response('Comment disliked')

        else:
            comment_to_like.like.add(user)
            comment_to_like.save()

            if (request.user != comment_to_like.user):
                # create a new notification
                notification = Notification.objects.create(
                    to_user=comment_to_like.user,
                    created_by=request.user,
                    content='liked your comment',
                    notification_type='like',
                    post=comment_to_like.post,
                )

                # send notification to the user
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'{comment_to_like.user.username}__notifications',
                    {
                        'type': 'new_notification',
                        'message': NotificationSerializer(notification).data
                    }
                )
            return Response('Comment liked')

    except Exception as e:
        message = {'detail': f'{e}'}
        return Response(message, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_by_user(request, username):
    user = CustomUser.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all().order_by('-updated')
    serializer_class = CollectionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collections_by_user(request, username):
    user = CustomUser.objects.get(username=username)

    if user == request.user:
        collection = Collection.objects.filter(user=user).order_by('-updated')

    else:
        collection = Collection.objects.filter(
            user=user, private=False).order_by('-updated')

    serializer = CollectionSerializer(collection, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_by_collection(request, username, slug):
    user = CustomUser.objects.get(username=username)

    if user == request.user:
        collection = Collection.objects.filter(user=user, slug=slug).first()
    else:
        collection = Collection.objects.filter(
            user=user, slug=slug, private=False).first()

    posts = Post.objects.filter(id__in=collection.posts.all())
    serializer = PostSerializer(posts, many=True)
    collection_serializer = CollectionSerializer(collection, many=False)
    return Response({'collection': collection_serializer.data, 'posts': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_to_collection(request, collection_slug, post_id):
    try:
        collection = Collection.objects.filter(
            slug=collection_slug, user=request.user).first()

        if collection is not None:
            post = Post.objects.get(id=post_id)
            if post not in collection.posts.all():
                collection.posts.add(post)
                collection.updated = Now()
                collection.save()

                if (request.user != post.user):
                    # create a new notification
                    notification = Notification.objects.create(
                        to_user=post.user,
                        created_by=request.user,
                        content='saved your post',
                        notification_type='save',
                        post=post,
                    )

                    # send notification to the user
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'{post.user.username}__notifications',
                        {
                            'type': 'new_notification',
                            'message': NotificationSerializer(notification).data
                        }
                    )
            else:
                return Response('Post already in the collection', status=status.HTTP_204_NO_CONTENT)

        serializer = CollectionSerializer(collection, many=False)
        return Response(serializer.data)

    except Exception as e:
        return Response(str(e))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_collection(request, collection_slug, post_id):
    try:
        collection = Collection.objects.filter(
            slug=collection_slug, user=request.user).first()

        if collection is not None:
            post = Post.objects.get(id=post_id)
            if post in collection.posts.all():
                collection.posts.remove(post)
            else:
                return Response('Post is not in the collection')

        serializer = CollectionSerializer(collection, many=False)
        return Response(serializer.data)

    except Exception as e:
        return Response(e)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_collection(request):
    user = request.user
    name = request.data['name']
    private = request.data['private']
    cover = request.data['cover']
    cover_url = request.data['cover_url']

    try:
        if cover != 'null':
            print('HI')
            collection = Collection.objects.create(
                user=user,
                name=name,
                private=private,
                cover=cover,
            )
        else:
            print('HI')
            collection = Collection.objects.create(
                user=user,
                name=name,
                private=private,
            )
        
        collection.cover_url = cover_url
        collection.save()

        serializer = CollectionSerializer(collection)

        return Response(serializer.data)
    except IntegrityError as e:
        return Response('A collection With the same name already exists', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_collection(request, slug):
    user = request.user

    try:
        collection = Collection.objects.filter(slug=slug, user=user).first()
        print(collection)
        if 'name' in request.data:
            collection.name=request.data['name']
            collection.save()
        if 'cover' in request.data:
            collection.cover=request.data['cover']
            collection.save()
        if 'private' in request.data:
            collection.private=request.data['private']
            collection.save()


        serializer = CollectionSerializer(collection)

        return Response(serializer.data)
    except IntegrityError as e:
        return Response('A collection With the same name already exists', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

