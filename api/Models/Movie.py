from __future__ import unicode_literals

from django.db import models
from .Genre import Genre


class Movie(models.Model):
    """
    Movie model : model for Movies
    """
    name = models.CharField(max_length=500)
    imdb_score = models.FloatField()
    popularity = models.FloatField()
    director = models.CharField(max_length=500)
    genre = models.ManyToManyField(Genre)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name
