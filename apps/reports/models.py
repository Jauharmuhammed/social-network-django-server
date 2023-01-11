from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.posts.models import Post

User = get_user_model()

# Create your models here.
# class Report(models.Model):
#     CHOICES = (
#         ('comment', 'comment'),
#         ('save', 'save'),
#         ('reply', 'reply'),
#         ('like', 'like'),
#         ('follow', 'follow'),
#     )

#     id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='report')
#     content = models.CharField(max_length=255)
#     notification_type = models.CharField(max_length=20, choices=CHOICES)
#     post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
#     read = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.content
