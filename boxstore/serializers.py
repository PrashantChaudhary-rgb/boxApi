from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'length', 'breadth', 'height','area', 'volume', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at', 'area', 'volume']
