from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.posts.models import Post, Collection

User = get_user_model()

# Create your models here.
class Notification(models.Model):
    CHOICES = (
        ('comment', 'comment'),
        ('save', 'save'),
        ('reply', 'reply'),
        ('like', 'like'),
        ('follow', 'follow'),
        ('invite', 'invite'),
    )

    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE, null=True, blank=True)
    followed_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='followed_by')
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content