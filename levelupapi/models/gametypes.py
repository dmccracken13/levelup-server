from django.db import models


class Game_Types(models.Model):

    types = models.CharField(max_length=50)