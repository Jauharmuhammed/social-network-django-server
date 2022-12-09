from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from apps.accounts.models import CustomUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import datetime

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('email', 'password', )


    def create(self, validated_data):
        email=validated_data['email'],
        username = email[0].split('@')[0]

        try:

            user = CustomUser.objects.create(
                email=validated_data['email'],
                username=username,
            )
        except:
            random = str(datetime.datetime.now().microsecond)[:4]
            username = str(email[0].split('@')[0]) + random
            print(username)

            user = CustomUser.objects.create(
                email=validated_data['email'],
                username=username,
            )

        
        user.set_password(validated_data['password'])
        user.save()

        return user