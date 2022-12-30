from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os
from urllib import request
from django.core.files import File

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, mobile_number, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=(self.normalize_email(email)).lower(),
            username = username,
            mobile_number = mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        user.save()

        return user

    def create_superuser(self, email, username, mobile_number, password=None):
        user = self.create_user(
            email,
            username = username,
            mobile_number = mobile_number,
            password=password,
        )
        
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True, null=True, blank=True)

    is_admin = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_number']

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_all_permissions(user=None):
        if user.is_superuser:
            return set()


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='social_network/profile_picture', max_length=255) #  , default='profile_picture/profile.png'
    profile_picture_url = models.URLField(blank=True, null=True, max_length=255)
    bio = models.TextField(null=True)
    followers = models.ManyToManyField(CustomUser, related_name='following', blank=True)


    def __str__(self):
        return str(self.user.email)

    def get_profile_pic(self):
        try:
            pic = self.profile_picture.url
        except:
            pic = 'https://res.cloudinary.com/dpofqivee/image/upload/v1672380610/social_network/profile_picture/profile_nloi7m.jpg'
        return pic

    def get_following(self):
        following = []
        for i in self.user.following.all():
            following.append(i.id)
        return following

    def get_full_name(self):
        if self.first_name or self.last_name:
            return str(f'{self.first_name} {self.last_name}')
        else: return self.username

    def get_followers_count(self):
        return self.followers.all().count()

    def get_followings_count(self):
        return self.user.following.all().count()

    def get_remote_image(self):
        if self.profile_picture_url and not self.profile_picture:
            result = request.urlretrieve(self.profile_picture_url[0])
            self.profile_picture.save(
                    os.path.basename(f'{self.profile_picture_url[0]}.jpg'),
                    File(open(result[0], 'rb'))
                    )
    
    def save(self, *args, **kwargs):
        self.get_remote_image()
        super().save(*args, **kwargs) 
