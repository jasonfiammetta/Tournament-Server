from django.db import models
from django.contrib.postgres.fields import ArrayField

from .user import User

class Tournament(models.Model):

  # https://docs.djangoproject.com/en/3.0/ref/models/fields/
  name = models.CharField(max_length=100)
  game = models.CharField(max_length=30)
  description = models.TextField(blank=True)
  # begun = models.BooleanField(default=False) # Not sure if I'll use these two booleans
  # over = models.BooleanField(default=False) # Considered a status enum instead too
  owner = models.ForeignKey(
      User,
      on_delete=models.CASCADE
  )
  # players = ArrayField(models.CharField(max_length=30)) # Array of strings for now. Might turn into a ForeignKey later

  def __str__(self):
    return f"'{self.name}' is a {self.game} tournament. Contact the TD at {self.owner.email}."

  def as_dict(self):
    """Returns dictionary version of Tournament models"""
    return {
        'id': self.id,
        'name': self.name,
        'game': self.game,
        'description': self.description,
        'owner': self.owner.id,
        'owner_email': self.owner.email
        # 'players': self.players
    }

  def owner_email(self):
    return self.owner.email

  def players(self):
    return self.player_set.all()
