from django.db import models
from apps.accounts.models import CustomUser, UserProfile
import uuid
from autoslug import AutoSlugField

from urllib import request
from django.core.files import File
import os

class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='social_network/posts', max_length=255)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.title

    def get_user_profile(self):
        profile = UserProfile.objects.filter(username=self.user.username).first()
        return profile

    # to get comment with parent is none and active is true
    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)  

    def get_comments_count(self):
        return self.comments.filter(active=True).count()    

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, related_name='posts',  on_delete=models.CASCADE)
    parent=models.ForeignKey("self", related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    like = models.ManyToManyField(CustomUser, related_name='liked_comments', blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return self.body

    def get_user_name(self):
        return self.user.username

    def get_user_profile_pic(self):
        return self.user.userprofile.get_profile_pic()

    def get_replies(self):
        return Comment.objects.filter(parent=self).filter(active=True)

    def get_replies_count(self):
        return Comment.objects.filter(parent=self).filter(active=True).count()

    def get_likes_count(self):
        return self.like.all().count()


class Collection(models.Model):
    name = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='name', max_length=100,)
    user = models.ForeignKey(CustomUser, related_name='collections', on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, blank=True)
    cover = models.ImageField(upload_to='social_network/collections', null=True, blank=True, max_length=255)
    cover_url = models.URLField(blank=True, null=True, max_length=255)

    collaborators = models.ManyToManyField(CustomUser)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    private = models.BooleanField(default=False)

    class Meta:
      unique_together = 'user', 'slug'

    def __str__(self):
        return self.slug

    def get_user_profile_pic(self):
        return self.user.userprofile.get_profile_pic()

    def get_remote_image(self):
        if self.cover_url and not self.cover:
            result = request.urlretrieve(self.cover_url)
            self.cover.save(
                    os.path.basename(f'{self.cover_url}.jpg'),
                    File(open(result[0], 'rb'))
                    )
    
    def save(self, *args, **kwargs):
        print('custom save function')
        self.get_remote_image()
        super().save(*args, **kwargs) 
