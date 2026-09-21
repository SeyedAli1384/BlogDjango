from django.db import models
import uuid
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Blog(models.Model):
    id = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True , blank=True)
    author = models.ForeignKey(User , on_delete=models.SET_NULL , null=True)
    title = models.CharField(max_length=30)
    Participants = models.ManyToManyField(User,related_name='participants' , blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    blog = models.TextField()
    source = models.TextField(null=True , blank=True)
    
    class Meta:
        ordering = ['-updated' , '-created']
    
    def __str__(self):
        return f"{self.title} created by {self.author}"
    
class Comments(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog , on_delete=models.SET_NULL , null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body[0:50]