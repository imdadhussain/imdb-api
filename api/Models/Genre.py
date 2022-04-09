from __future__ import unicode_literals

from django.db import models


class Genre(models.Model):
    """
    Genre model : Table for movie Genres
    """
    name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


