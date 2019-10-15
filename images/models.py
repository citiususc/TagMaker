from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from djongo import models

from users.models import Team

PRIMITIVES_CHOICES = [("Box", _("Box"),),
                      ("Point", _("Point")),
                      ("Curve", _("Curve")),
                      ("Polygon", _("Polygon"))]


class Dataset(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)


class Image(models.Model):
    name_unique = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    checksum = models.CharField(max_length=64)
    path = models.CharField(max_length=1024)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="images")


class Experiment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=1024)
    date = models.DateField(auto_now_add=True, blank=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class AnnotationType(models.Model):
    name = models.CharField(max_length=64, blank=True)
    state = models.BooleanField(default=False)
    color = models.CharField(max_length=7, null=False)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    primitive = models.CharField(max_length=10, choices=PRIMITIVES_CHOICES,
                                 null=False)


class ImageTag(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    check_by = models.ForeignKey(User, related_name='check_by', on_delete=models.CASCADE, blank=True)


class IndividualTag(models.Model):
    type = models.ForeignKey(AnnotationType, related_name="type", on_delete=models.CASCADE)
    image_tag = models.ForeignKey(ImageTag, related_name="individual_tags", on_delete=models.CASCADE)


class IndividualTagPoint(IndividualTag):
    x = models.FloatField(blank=True)
    y = models.FloatField(blank=True)


class IndividualTagBox(IndividualTag):
    x_top_left = models.FloatField(blank=True)
    y_top_left = models.FloatField(blank=True)
    width = models.FloatField(blank=True)
    height = models.FloatField(blank=True)


class IndividualTagCurve(IndividualTag):
    points = models.ArrayModelField(model_container=IndividualTagPoint)
    isClosed = models.BooleanField(default=False)

