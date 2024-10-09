import uuid
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField() 
    url_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    expiration = models.DateTimeField(null=True, blank=True)
    max_views = models.IntegerField(null=True, blank=True)  
    views = models.IntegerField(default=0)