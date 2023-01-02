from django.shortcuts import render

from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes, APIView, parser_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from .models import Post, Tag, Comment
from .serializers import PostSerializer, TagSerializer, CommentSerializer
from apps.accounts.models import CustomUser


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
            if tag.strip() == '': continue

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
            if tag.strip() == '': continue
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
    comments = Comment.objects.filter(post=id, parent=None).order_by('-created')
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
            return Response('Comment liked')
            
    except Exception as e:
        message = {'detail':f'{e}'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_by_user(request, username):
    user = CustomUser.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
