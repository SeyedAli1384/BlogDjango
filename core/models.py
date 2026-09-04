from django.db import models
import uuid

class Blog(models.Model):
    id = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    author = models.CharField(max_length=20 , null=True , blank=True) 
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    blog = models.TextField()
    
    def __str__(self):
        return f"{self.title} created by {self.author}"