from django.db import models

from .tournament import Tournament

class Player(models.Model):
    name = models.CharField(max_length=30)
    tournament = models.ForeignKey(
      Tournament,
      on_delete=models.CASCADE,
      related_name='players'
    )

    def __str__(self):
        return f"{self.name}"
