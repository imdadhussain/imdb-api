from django.db import models

from .User import BaseAbstract


class Genre(BaseAbstract):
    """
    Genre model : Table for movie Genres
    """
    name = models.CharField(max_length=500, unique=True, db_index=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name
