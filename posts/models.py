from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()

    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='posts')

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class IdempotencyRecord(models.Model):
    key=models.CharField(max_length=255, unique=True)
    request_hash= models.CharField(max_length=64, blank=True, default="")
    response_data=models.JSONField()
    status_code=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    
