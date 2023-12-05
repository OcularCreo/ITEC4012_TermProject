from django.contrib.postgres.fields import ArrayField
import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


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


"""
# user model
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=75)

    def __str__(self):
        return f'{self.username} {self.password}'
"""

# junction table for users and recipes
class UserRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    favourite = models.BooleanField(default=False)
    playlist_name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.recipe} {self.favourite} {self.playlist_name}'