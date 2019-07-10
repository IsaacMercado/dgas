from rest_framework import serializers
from .models import Vehiculo, Carga, Cola, Combustible, Estacion


class VehiculoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehiculo
        fields = ('placa',)


class CargaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carga
        fields = ('id', 'cantidad', 'estacion', 'vehiculo', 'tipo_combustible')


class EstacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estacion
        fields = ('id', 'nombre', 'municipio', 'direccion')


class CombustibleSerializer(serializers.ModelSerializer):

    estacion = EstacionSerializer()
    total_cola = serializers.IntegerField()

    class Meta:
        model = Combustible
        fields = ('id', 'tipo_combustible', 'estacion', 'nota',
                  'cantidad_maxima_por_vehiculo', 'cantidad_vehiculos', 'created_at', 'last_modified_at', 'total_cola')


class ColaSerializer(serializers.ModelSerializer):

    #combustible = CombustibleSerializer()
    vehiculo = VehiculoSerializer()
    #vehiculo = serializers.PrimaryKeyRelatedField(many=False, source='vehiculo.placa')
    #vehiculo = serializers.ReadOnlyField(source='vehiculo.placa')

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado', 'combustible')


class ColaCrudSerializer(serializers.ModelSerializer):

    #vehiculo = VehiculoSerializer()

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado', 'combustible')


class ColaPublicoSerializer(serializers.ModelSerializer):

    vehiculo = VehiculoSerializer()

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado')
