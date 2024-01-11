from django_filters import rest_framework as filters
from .models import Box

class BoxFilter(filters.FilterSet):
  
    class Meta:
        model = Box
        fields = {
            'length': ['gt', 'lt'],
            'breadth': ['gt', 'lt'],
            'height': ['gt', 'lt'],
            'area': ['gt', 'lt'],
            'volume': ['gt', 'lt'],
            'created_by__username': ['exact'],
            'created_at': ['gt', 'lt'],
        }
    
