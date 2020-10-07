from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    name = models.CharField(max_length=60,blank=True)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True,null=True,upload_to='images/')
