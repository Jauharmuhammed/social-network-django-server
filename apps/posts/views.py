from django.shortcuts import render

from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes, APIView, parser_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser

from .models import Post
from .serializers import PostSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([ FormParser, MultiPartParser])
def create_post(request):
    data = request.data
    user = request.user

    print('data',request.FILES['image'])

    # post = Post.objects.create(
    #     user = user,
    #     title = data.get('title'),
    #     description = data.get('description'),
    #     image = data.get('image'),
    # )

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PostSerializer
    parser_class=(FileUploadParser,)

    def post(self, *args, **kwargs):
        image=self.request.FILES.get('image')
        print('image: ' ,image)
        return Response('')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created')
    serializer_class = PostSerializer
