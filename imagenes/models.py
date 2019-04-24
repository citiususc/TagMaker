from djongo import models
from usuarios.models import Equipo
from anotaciones.models import Anotacion

class Dataset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True)
    imagenes = models.CharField(max_length=100,unique=True)

class Experimento(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True)
    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    equipo = models.OneToOneField(Equipo, on_delete=models.CASCADE)
    anotaciones = models.ManyToManyField(Anotacion)