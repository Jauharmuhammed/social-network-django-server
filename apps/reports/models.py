from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.posts.models import Post, Comment

User = get_user_model()

class Report(models.Model):
    TYPE_CHOICES = (
        ('post', 'post'),
        ('comment', 'comment'),
        ('user', 'user'),
    )
    REASON_CHOICES = (
        ('spam_or_fake', 'spam_or_fake'),
        ('adult_content', 'adult_content'),
        ('hate_speech', 'hate_speech'),
        ('intellectual_property_violation', 'intellectual_property_violation'),
        ('not_liked', 'not_liked'),
    )

    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportings')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reason = models.CharField(max_length=155, choices=REASON_CHOICES)
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reports')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
      unique_together = 'reported_by', 'post'
      unique_together = 'reported_by', 'comment'
      unique_together = 'reported_by', 'user', 'type'
    
    def __str__(self):
        if self.type == 'user':
            return f'{self.user} reported by {self.reported_by}'
        else:
            return f"{self.user}'s {self.type} reported by {self.reported_by}"
