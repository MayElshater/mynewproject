from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chatbot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    personality = models.TextField(default="Friendly")  
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentChunk(models.Model):
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='document_chunks')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=50, unique=True, blank=True, null=True)
    chatbot_quota = models.IntegerField(default=5)  # Example quota