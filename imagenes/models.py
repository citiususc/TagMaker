from djongo import models
from usuarios.models import Equipo
from anotaciones.models import TagPoint, TagBox

class Image(models.Model):
    name = models.CharField(max_length=64)
    checksum = models.CharField(max_length=64)
    path = models.CharField(max_length=1024)

class Dataset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True)
    images = models.ManyToManyField(Image)

class Experimento(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE)
    tags_point = models.ManyToManyField(TagPoint)
    tags_box = models.ManyToManyField(TagBox)
