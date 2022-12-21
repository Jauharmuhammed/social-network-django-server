from django.shortcuts import render

from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes, APIView, parser_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    image = request.data['image']
    title = request.data['title']
    description = request.data['description']

    tags = request.data['tags'].split(',')


    post = Post.objects.create(
        user=user,
        image=image,
        title=title,
        description=description,
    )

    if tags is not None:
        for tag in tags:
            tag_instance = Tag.objects.filter(name__iexact=tag).first()
            if not tag_instance:
                tag_instance = Tag.objects.create(name=tag)
            post.tags.add(tag_instance)
    post.save()

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

    # serializer = PostSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
