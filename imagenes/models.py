from djongo import models
from usuarios.models import Equipo

class Coordinates(models.Field):
    x = models.FloatField()
    y = models.FloatField()
    class Meta:
        abstract = True

"""
class TagImage(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    user = models.ForeignKey('User')
    #experiment=models.ManyToOneRel(Experimento, on_delete=models.CASCADE)
    check_by = models.ForeignKey('User')
    tags_points = models.ManyToManyField(TagPoint)
    tags_rectangles=models.ManyToManyField(TagBox)

"""

class TagPoint(models.Model):
    name = models.CharField(max_length=64)
    coordinates = Coordinates()

class TagBox(models.Model):
    name = models.CharField(max_length=64)
    coordinates_up = Coordinates()
    coordinates_down = Coordinates()

class Image(models.Model):
    name = models.CharField(max_length=64)
    checksum = models.CharField(max_length=64)
    name_unique = models.CharField(max_length=64)
    path = models.CharField(max_length=1024)

class Dataset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)

class Experimento(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE)
    tagsPoint = models.ManyToManyField(TagPoint, blank=True)
    tagsBox = models.ManyToManyField(TagBox, blank=True)
