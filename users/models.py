from djongo import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=1024,blank=True)
    users = models.ManyToManyField(User)