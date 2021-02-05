from django.db import models


class Event_Gamers(models.Model):

    event = models.ForeignKey("Events", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamers", on_delete=models.CASCADE)