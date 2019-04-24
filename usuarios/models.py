from djongo import models
from django.contrib.auth.models import User

class Equipo(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=1024)
    users = models.ManyToManyField(User)

    class Meta:
        abstract = False
