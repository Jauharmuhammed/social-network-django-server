from django.db import models
from apps.accounts.models import CustomUser, UserProfile
import uuid

class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='social_network/posts')
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    parent=models.ForeignKey("self", related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    like = models.ManyToManyField(UserProfile, blank=True)
    
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