from django.contrib.postgres.fields import ArrayField
from django.db import models
import datetime
from django.utils.translation import gettext as _


# Create your models here.

# recipe model
class Recipe(models.Model):

    name = models.CharField(_("name"), max_length=255)
    minutes = models.IntegerField(_("minutes"))
    submitted = models.DateField(_("submitted"))
    tags = models.CharField(_("tags"), max_length=255)
    nutrition = models.CharField(_("nutrition"), max_length=255)
    steps = models.CharField(_("steps"), max_length=255)
    step_num = models.IntegerField(_("n_steps"))
    ingreds = models.CharField(_("ingredients"), max_length=255)
    ingred_num = models.IntegerField(_("n_ingredients"))

    def __str__(self):
        return f'{self.name} {self.minutes} {self.submitted} {self.tags} {self.nutrition} {self.steps} {self.step_num} {self.ingreds} {self.ingred_num}'


# user model
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=75)

    def __str__(self):
        return f'{self.username} {self.password}'