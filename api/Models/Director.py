from django.db import models

from .User import BaseAbstract


class Director(BaseAbstract):
    """
    Director model : Table for movie director
    """
    name = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"

    def __str__(self):
        return self.name
