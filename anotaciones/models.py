from djongo import models

class Coordinates(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    class Meta:
        abstract = True

class TagPoint(models.Model):
    name = models.CharField(max_length=30)
    coordinates=Coordinates()

class TagBox(models.Model):
    name = models.CharField(max_length=30)
    coordinates_up_left=Coordinates()
    coordinates_down_right=Coordinates()

"""
class TagImage(models.Model):
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    user = models.ForeignKey('User')
    #experiment=models.ManyToOneRel(Experimento, on_delete=models.CASCADE)
    check_by = models.ForeignKey('User')
    tags_points = models.ManyToManyField(TagPoint)
    tags_rectangles=models.ManyToManyField(TagBox)

"""