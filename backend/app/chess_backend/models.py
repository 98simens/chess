from django.db import models
from main.models import User

# Create your models here.

class Move(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    move_from = models.CharField(max_length=10)
    move_to = models.CharField(max_length=10)
    made_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player')

class Bet(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bet_winner')

class Game(models.Model):
    key = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    fen = models.CharField(max_length=4096)
    white = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='white_player')
    black = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='black_player')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='winning_player')
    is_over = models.BooleanField(default=False)
    moves = models.ManyToManyField(Move)
    bets = models.ManyToManyField(Bet)
    