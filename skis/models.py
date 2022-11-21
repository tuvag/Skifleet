from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Ski(models.Model):
    ski_number = models.CharField(max_length = 64)
    technique = models.CharField(max_length = 64)
    grind = models.CharField(max_length = 64)
    brand = models.CharField(max_length = 64)
    img = models.ImageField(upload_to='images/', blank=True)
    url_img = models.URLField()
    color_tag = models.IntegerField()
    notes = models.CharField(max_length = 256)
    ski_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")

class Technique(models.Model):
    technique = models.CharField(max_length=64)

class Testski(models.Model):
    ski = models.ForeignKey(Ski, on_delete=models.CASCADE, blank=True, null=True, related_name="testski")
    rank = models.IntegerField()

class Skitest(models.Model):
    date_of_test = models.DateField()
    temprature = models.IntegerField()
    humidity = models.IntegerField(null=False)
    location = models.CharField(max_length = 64)
    snow_type = models.CharField(max_length = 64)
    notes = models.CharField(max_length= 256)
    testski = models.ManyToManyField(Testski)
    tester = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="tester")

