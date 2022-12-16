from django.db import models
from apps.accounts.models import CustomUser

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='social_network/posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name
