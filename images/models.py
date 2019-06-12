from djongo import models
from users.models import Team
from django.contrib.auth.models import User

class Image(models.Model):
    name_unique = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    checksum = models.CharField(max_length=64)
    path = models.CharField(max_length=1024)

class Dataset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)

class Experiment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class TagPoint(models.Model):
    name = models.CharField(max_length=64)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    x = models.FloatField(blank=True)
    y = models.FloatField(blank=True)

class TagBox(models.Model):
    name = models.CharField(max_length=64)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    x_top_left = models.FloatField(blank=True)
    y_top_left = models.FloatField(blank=True)
    x_bottom_right = models.FloatField(blank=True)
    y_bottom_right = models.FloatField(blank=True)


class TagImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    check_by = models.ForeignKey(User, related_name='check_by', on_delete=models.CASCADE, blank=True)
    tags_points = models.ManyToManyField(TagPoint)
    tags_boxes = models.ManyToManyField(TagBox)
