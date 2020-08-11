from django.db import models

from .tournament import Tournament
from .player import Player

class Match(models.Model):
    tournament = models.ForeignKey(
      Tournament,
      on_delete=models.CASCADE
    )
    player_1 = models.ForeignKey(
      Player,
      on_delete=models.CASCADE,
      related_name='player_1',
      null=True,
      blank=True
    )
    player_2 = models.ForeignKey(
      Player,
      on_delete=models.CASCADE,
      related_name='player_2',
      null=True,
      blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tournament.game} match between {self.player_1} and {self.player_2}"
