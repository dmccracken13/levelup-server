from django.db import models


class Games(models.Model):

    title = models.CharField(max_length=50)
    game_type = models.ForeignKey("Game_Types", on_delete=models.CASCADE)
    gamer = models.ForeignKey("Gamers", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    description = models.CharField(max_length=200)