from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics
from apps.accounts.models import CustomUser
from .serializers import UserSerializer, RegisterSerializer

import datetime

from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'api/token',
        'api/token/refresh',
    ]
    return Response(routes)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GoogleAuthApiView(APIView):
    def post(self, request):
        token = request.data['token']

        googleUser = id_token.verify_token(token, GoogleRequest())

        if not googleUser:
            return Response('authentication failed')

        user = CustomUser.objects.filter(email=googleUser['email']).first()

        if not user:
            email=googleUser['email'],
            print(email)
            print(type(email))
            username = email[0].split('@')[0]


            try:
                user = CustomUser.objects.create(
                    first_name = googleUser['given_name'],
                    last_name = googleUser['family_name'],
                    email = googleUser['email'],
                    username = username
                )
            except:
                random = str(datetime.datetime.now().microsecond)[:4]
                username = str(email[0].split('@')[0]) + random
                print(username)

                user = CustomUser.objects.create(
                    first_name = googleUser['given_name'],
                    last_name = googleUser['family_name'],
                    email = googleUser['email'],
                    username = username
                )


            user.set_password(token)
            user.save()

        token = get_tokens_for_user(user)
        
        return Response(token)