from rest_framework import serializers
from .models import Vehiculo, Carga, Cola, Combustible, Estacion, Rebotado, RebotadoBloqueado


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
        fields = ('usuario', 'placa', 'cedula', 'tipo_vehiculo', 'organizacion', 'paso_preferencial', 'cilindros','created_at', 'bloqueado')


class CargaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carga
        fields = ('id', 'cantidad', 'estacion', 'vehiculo', 'tipo_combustible')


class EstacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estacion
        fields = ('id', 'nombre', 'municipio', 'direccion', 'operativa',)


class CombustibleSerializer(serializers.ModelSerializer):

    estacion = EstacionSerializer(read_only=True)
    total_cola = serializers.IntegerField(read_only=True)
    total_rebotados = serializers.IntegerField(read_only=True)
    total_colas_cantidad = serializers.IntegerField(read_only=True)
    total_surtidos = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

    class Meta:
        model = Combustible
        fields = ('id',
                  'estacion',
                  'nota',
                  'created_at',
                  'last_modified_at',
                  'total_cola',
                  'total_rebotados',
                  'total_surtidos',
                  'total_colas_cantidad'
        )


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

class RebotadoBloqueadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RebotadoBloqueado
        fields = ('id', 'combustible', 'vehiculo')
