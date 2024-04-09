# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Tactic(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=True)
    exercises = models.IntegerField(default=0, null=True)
    performance = models.IntegerField(default=0.0, null=True)
    training_set = models.CharField(max_length=100)
    duration = models.FloatField(default=0)
    date = models.DateField()

    def recompute_duration(self):
        amount = 0
        if self.training_set == 'Puzzle Storm':
            amount = 4
        elif self.training_set == 'Puzzle Racer':
            amount = 2
        self.duration = amount * self.attempts.count()
        self.save()

    def __str__(self):
        return f"{self.training_set} - {self.date}"

class TacticAttempt(models.Model):
    tactic = models.ForeignKey('Tactic', on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rithm = models.CharField(max_length=20)  # Blitz, Rapid, Clasica, OTB
    score = models.FloatField(default=0)
    games = models.IntegerField(default=0)
    elo = models.IntegerField(default=0)
    link = models.CharField(max_length=100)
    plataform = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)
    date = models.DateField()

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_type = models.CharField(max_length=20)  # Aperturas, Estrategia, Analisis
    theme = models.CharField(max_length=100)
    notes = models.CharField(max_length=256)
    duration = models.IntegerField(default=0)
    date = models.DateField()
