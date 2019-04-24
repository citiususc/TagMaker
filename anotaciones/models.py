from djongo import models

class Anotacion(models.Model):
    anotaciones = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)
    #coordenadas