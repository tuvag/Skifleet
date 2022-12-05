from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField


class User(AbstractUser):
    pass

class Technique(models.Model):
    technique = models.CharField(max_length=64)

    def __str__(self):
        return self.technique

class Ski(models.Model):
    # ski_number: is this a unique number? if so, add "unique=true". it could also be 
    # used as the primary key, but 
    ski_number = models.IntegerField()

    # technique: do you want the technique to be a FK to the Technique class? 
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE, related_name="style")

    # grind, brand: should these be FKs? (if it's easier for now to have this be a string,
    # keep it that way for the time being)
    grind = models.CharField(max_length = 64)
    brand = models.CharField(max_length = 64)

    img = models.ImageField(upload_to='images/', blank=True)
    url_img = models.URLField()

    # is this an RGB value? 
    color_tag = ColorField(default='#ffffff')

    notes = models.CharField(max_length = 256)

    # the related name should be "skis_owned". If you have given a user, you
    # can get all the skis that she owns by saying "user.skis_owned.all()" or 
    # you can filter based on, say, grind: "user.skis_owner.filter(grind="blahblah").
    ski_owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="skies_owned")

    def save(self, *args, **kwargs):
        if self.url_img and not self.img:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.url_img).read())
            img_temp.flush()
            self.img.save(f"image_{self.pk}", File(img_temp))
        super(Ski, self).save(*args, **kwargs)


# super confusing to have Skitest and Testski. Can you think of a better name
# for both? SkiTest is something like "Setting". And then "Testski" is think would
# be best called "SkiTest". Don't start a class with "Test"; it's magic to django. 

class Setting(models.Model):
    date = models.DateField()
    temprature = models.IntegerField()
    humidity = models.IntegerField()
    location = models.CharField(max_length = 64)
    snow_type = models.CharField(max_length = 64)
    notes = models.CharField(max_length= 256)
    skis = models.ManyToManyField(Ski, related_name="settings", through='SkiTest')
    tester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skies_tested")

class SkiTest(models.Model):
    ski = models.ForeignKey(Ski, on_delete=models.CASCADE, related_name="ski_tested")
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, related_name="related_test")
    rank = models.IntegerField()

