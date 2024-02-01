# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class PuzzleRun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_1 = models.IntegerField(default=0, null=True)
    score_2 = models.IntegerField(default=0, null=True)
    score_3 = models.IntegerField(default=0, null=True)
    puzzle = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)
    date = models.DateField()

class Tactic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    exercises = models.IntegerField(default=0)
    performance = models.IntegerField(default=0.0)
    training_set = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    date = models.DateField()

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
