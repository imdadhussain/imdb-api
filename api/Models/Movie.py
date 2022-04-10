from django.db import models

from .Director import Director
from .Genre import Genre
from .User import BaseAbstract


class Movie(BaseAbstract):
    """
    Movie model : model for Movies
    """
    name = models.CharField(max_length=500)
    imdb_score = models.FloatField()
    popularity = models.FloatField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.name
