from rest_framework import serializers

from api.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """Serializes a Genre"""

    class Meta:
        model = Genre
        fields = '__all__'
