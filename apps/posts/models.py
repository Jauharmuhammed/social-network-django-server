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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.title

    def get_user_profile(self):
        profile = UserProfile.objects.filter(username=self.user.username).first()
        return profile