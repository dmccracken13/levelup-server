from django.db import models


class GameType(models.Model):

    types = models.CharField(max_length=50)