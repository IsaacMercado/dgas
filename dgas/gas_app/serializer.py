from rest_framework import serializers
from .models import Vehiculo, Carga


class VehiculoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehiculo
        fields = ('placa', 'cilindros')


class CargaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carga
        fields = ('id', 'cantidad', 'estacion', 'vehiculo')
