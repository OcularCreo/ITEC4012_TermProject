from django.db import models
import datetime
from django.utils.translation import gettext as _

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=75)

    def __str__(self):
        return f'{self.username} {self.password}'

"""
class Recipe(models.Model):

    name = models.CharField(_("name"), max_length=255)
    minutes = models.IntegerField(_("minutes"))
    submitted = models.DateField(_("submitted"))
    tags = models.TextField(_("tags"))
    nutrition = models.TextField(_("nutrition"))
    steps = models.TextField(_("steps"))
    step_num = models.IntegerField(_("n_steps"))
    ingreds = models.TextField(_("ingredients"))
    ingred_num = models.IntegerField(_("n_ingredients"))
    
"""
