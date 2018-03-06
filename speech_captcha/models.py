# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Corpus(models.Model):
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20)
    # sentences = models.ManyToManyField(Sentence)

class Sentence(models.Model):
    transcript = models.TextField()
    corpus = models.ForeignKey(Corpus)

class Utterance(models.Model):
    utterance = models.FileField()
    transcript = models.ForeignKey(Sentence)