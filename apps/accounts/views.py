from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from rest_framework import generics
from rest_framework import status
from apps.accounts.models import CustomUser, UserProfile
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer

import datetime
from decouple import config

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

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


def get_tokens_for_user(user):
    print('called')
    refreshToken = RefreshToken.for_user(user)
    accessToken = refreshToken.access_token

    decodeAccess = jwt.decode(str(accessToken), config('SECRET_KEY'), algorithms=["HS256"]);
    decodeRefresh = jwt.decode(str(refreshToken), config('SECRET_KEY'), algorithms=["HS256"]);

    # add payload here!!
    decodeAccess['username'] = user.username
    decodeAccess['is_admin'] = user.is_superuser
    decodeAccess['profile_pic'] = user.userprofile.get_profile_pic()
    decodeAccess['followers'] = user.userprofile.get_followers_count()
    decodeAccess['name'] = user.userprofile.get_full_name()

    
    decodeRefresh['username'] = user.username
    decodeRefresh['is_admin'] = user.is_superuser
    decodeRefresh['profile_pic'] = user.userprofile.get_profile_pic()
    decodeRefresh['followers'] = user.userprofile.get_followers_count()
    decodeRefresh['name'] = user.userprofile.get_full_name()

    #encode
    encodedAccess = jwt.encode(decodeAccess, config('SECRET_KEY'), algorithm="HS256")
    encodedRefresh = jwt.encode(decodeRefresh, config('SECRET_KEY'), algorithm="HS256")

    token = {
        'refresh': str(encodedRefresh),
        'access': str(encodedAccess),
    }
    
    return token 

class RegisterView(APIView):
    def post(self, request):
        print(request.data)

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.errors)

            user = CustomUser.objects.filter(email = serializer.data['email']).first()

            #user activation using email id
            current_site = get_current_site(request)
            mail_subject = 'Activation email for your account'
            message = render_to_string('account_verification_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = user.email
            send_mail(mail_subject, message, 'showyourworkonline@gmail.com', [to_email], fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
            user.is_active = True
            user.save()

            user_profile = UserProfile.objects.get(user=user)
            user_profile.profile_picture_url = googleUser['picture'],
            user_profile.save()


        token = get_tokens_for_user(user)
        
        return Response(token)


class EmailVerifyView(APIView):
    def post(self, request):
        uidb64 = request.data['uidb64']
        token = request.data['token']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            token = get_tokens_for_user(user)

            return Response(token, status=status.HTTP_200_OK)

        else:
          return Response('verification failed', status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordView(APIView):
    def post(self, request):
        email = (request.data['email']).lower()
        print(email)
        try:
            user = CustomUser.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Password change request'
            message = render_to_string('forgot-password-email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_mail(mail_subject, message, 'showyourworkonline@gmail.com', [to_email], fail_silently=False)

            return Response(email, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('No account is registered with email id you entered!', status=status.HTTP_400_BAD_REQUEST)
            
            

class ForgotPasswordVerifyView(APIView):

    def post(self, request):

        uidb64 = request.data['uidb64']
        token = request.data['token']

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            
            return Response(uid, status=status.HTTP_200_OK)
        else:
            return Response('Verification failed', status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(APIView):
    def post(self, request):
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        uid = request.data['uid']


        try:
            if password == confirm_password:
                user = CustomUser.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                return Response('Password changed successfully', status=status.HTTP_200_OK)
            else:
                return Response('Passwords does not match', status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response('Request failed', status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):
    def post(self, request):
        mobile_number = request.data['mobile_number']

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
          try:
            request.session['mobile_number'] = mobile_number

            account_sid = config('TWILIO_ACCOUNT_SID')
            auth_token = config('TWILIO_AUTH_TOKEN')
            client = Client(account_sid,auth_token)

            verification = client.verify \
                .services('VAea529285dd3bdf25ceac9b9de80eb89c') \
                .verifications \
                .create(to='+91'+mobile_number, channel='sms')

            print(verification.status)
            return Response({'message':'OTP send successfully', "mobile_number":mobile_number})
          except TwilioRestException:
            return Response(TwilioRestException)
        else:
            return Response('Phone Number is not Registered', status=status.HTTP_400_BAD_REQUEST)



class LoginWithOtpView(APIView):
    def post(self, request):
        otp = request.data['otp']
        mobile_number= request.data['mobile_number']

        print(otp, mobile_number)

        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services('VAea529285dd3bdf25ceac9b9de80eb89c')\
            .verification_checks \
            .create(to='+91'+mobile_number, code=otp)

        print(verification_check.status)

        if verification_check.status == 'approved':

            user = CustomUser.objects.get(mobile_number=mobile_number)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response(token)
                
            else:
                return Response('An error occured, please contact customer support')
        else:
            return Response('OTP is incorrect', status=status.HTTP_400_BAD_REQUEST)

  

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        user = CustomUser.objects.get(username=username)

        if request.user in user_profile.followers.all():
            is_following = True
        else:
            is_following = False

        is_following = True  if request.user in user_profile.followers.all() else False
        is_current_user = True  if request.user == user else False

        


        serializer = UserProfileSerializer(user_profile, many=False)
        data = dict(serializer.data)

        # # follwing list
        # following = user.following.all()
        data.update({'is_following':is_following, 'is_current_user': is_current_user})
        return Response(data )
        
    except Exception as e:
        message = {'detail':f'{e}'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    user = request.user
    try:
        user_to_follow = UserProfile.objects.get(username=username)
        
        if user == user_to_follow.user:
            print('true')
            return Response("You can't follow yourself")

        if user in user_to_follow.followers.all():
            user_to_follow.followers.remove(user)
            user_to_follow.save()
            return Response('User unfollowed')
        
        else:
            user_to_follow.followers.add(user)
            user_to_follow.save()
            return Response('User followed')
            
    except Exception as e:
        message = {'detail':f'{e}'}
        return Response(message,status=status.HTTP_204_NO_CONTENT)

        