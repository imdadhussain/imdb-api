from rest_framework import serializers

from api.models import Director


class DirectorSerializer(serializers.ModelSerializer):
    """Serializes a Director"""

    class Meta:
        model = Director
        fields = '__all__'
