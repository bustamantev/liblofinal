from rest_framework import serializers
from core.models import CategoriaLibro, Libro

class CategoriaLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaLibro
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
