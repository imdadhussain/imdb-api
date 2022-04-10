from rest_framework import serializers

from .GenreSerializer import GenreSerializer
from .DirectorSerializer import DirectorSerializer

from api.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """Serializes for Movie"""
    genre = GenreSerializer(many=True)
    director = DirectorSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
