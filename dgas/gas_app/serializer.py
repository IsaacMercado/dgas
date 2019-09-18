from rest_framework import serializers
from .models import Vehiculo, Carga, Cola, Combustible, Estacion, Rebotado


class VehiculoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehiculo
        fields = ('placa',)


class VehiculoUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehiculo
        fields = ('usuario', 'placa', 'cedula', 'tipo_vehiculo', 'cilindros')


class VehiculoSupervisorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehiculo
        fields = ('usuario', 'placa', 'cedula', 'tipo_vehiculo', 'cilindros','created_at', 'bloqueado')

class CargaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carga
        fields = ('id', 'cantidad', 'estacion', 'vehiculo', 'tipo_combustible')


class EstacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estacion
        fields = ('id', 'nombre', 'municipio', 'direccion', 'operativa',)


class CombustibleSerializer(serializers.ModelSerializer):

    estacion = EstacionSerializer()
    total_cola = serializers.IntegerField()
    total_rebotados = serializers.IntegerField()
    total_surtidos = serializers.FloatField()

    class Meta:
        model = Combustible
        fields = ('id', 'tipo_combustible', 'estacion', 'nota', 'activar_cola',
                  'cantidad_maxima_por_vehiculo', 'cantidad_vehiculos', 'created_at', 'last_modified_at', 'total_cola', 'total_rebotados', 'total_surtidos')


class ColaSerializer(serializers.ModelSerializer):

    #combustible = CombustibleSerializer()
    vehiculo = VehiculoSerializer()
    #vehiculo = serializers.PrimaryKeyRelatedField(many=False, source='vehiculo.placa')
    #vehiculo = serializers.ReadOnlyField(source='vehiculo.placa')

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado', 'combustible', 'cantidad')


class ColaCrudSerializer(serializers.ModelSerializer):

    #vehiculo = VehiculoSerializer()

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado', 'combustible', 'cantidad')


class ColaPublicoSerializer(serializers.ModelSerializer):

    vehiculo = VehiculoSerializer()

    class Meta:
        model = Cola
        fields = ('id', 'vehiculo', 'cargado')


class RebotadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rebotado
        fields = ('id', 'combustible', 'vehiculo')
