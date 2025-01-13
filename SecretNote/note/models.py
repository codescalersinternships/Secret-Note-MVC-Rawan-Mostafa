import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField() 
    url_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    expiration = models.DateTimeField(null=True, blank=True)
    max_views = models.IntegerField(default=1)  
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.content
    
    def is_expired(self):
        return self.expiration and timezone.now() >= self.expiration
    