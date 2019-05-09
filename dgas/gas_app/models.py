from django.db import models
from model_utils import Choices
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import Sum
from dgas.users.models import GasUser

COMBUSTIBLE_TIPO_CHOICES = Choices('91', '95', 'Gasoil')
CILINDROS_CHOICES = Choices('1', '2', '3', '4', '6', '8')


class Estacion(models.Model):
    usuario = models.ForeignKey(GasUser, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    capacidad_91 = models.PositiveIntegerField(default=0)
    reserva_91 = models.PositiveIntegerField(default=0)
    capacidad_95 = models.PositiveIntegerField(default=0)
    reserva_95 = models.PositiveIntegerField(default=0)
    capacidad_gasoil = models.PositiveIntegerField(default=0)
    reserva_gasoil = models.PositiveIntegerField(default=0)
    operativa = models.BooleanField('Abierto', default=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    created_by = UserForeignKey(auto_user_add=True, related_name='estacion_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='estacion_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

    @property
    def disponible91(self):

        porcentaje = 0
        bar_color = 1

        total = Combustible.objects.filter(estacion_id=self.id, tipo_combustible='91').aggregate(Sum('cantidad'))
        total_cargado = Carga.objects.filter(estacion_id=self.id, tipo_combustible='91').aggregate(Sum('cantidad'))

        if total_cargado['cantidad__sum'] is None:
            tc = float(0.0)
        else:
            tc = total_cargado['cantidad__sum']

        if total['cantidad__sum']:
            total_publico = total['cantidad__sum'] - self.reserva_91
            total_disponible = total_publico - tc
            porcentaje = (total_disponible/total_publico)*100
            if porcentaje < 25:
                bar_color = 1
            elif 25 <= porcentaje <= 50:
                bar_color = 2
            elif porcentaje > 50:
                bar_color = 3
        else:
            return [0, 0, 0]

        return [total_disponible,porcentaje, bar_color]

    @property
    def disponible95(self):

        porcentaje = 0
        bar_color = 1

        total = Combustible.objects.filter(estacion_id=self.id, tipo_combustible='95').aggregate(Sum('cantidad'))
        total_cargado = Carga.objects.filter(estacion_id=self.id, tipo_combustible='95').aggregate(Sum('cantidad'))

        if total_cargado['cantidad__sum'] is None:
            tc = float(0.0)
        else:
            tc = total_cargado['cantidad__sum']

        if total['cantidad__sum']:
            total_publico = total['cantidad__sum'] - self.reserva_95
            total_disponible = total_publico - tc
            porcentaje = (total_disponible / total_publico) * 100
            if porcentaje < 25:
                bar_color = 1
            elif 25 <= porcentaje <= 50:
                bar_color = 2
            elif porcentaje > 50:
                bar_color = 3
        else:
            return [0, 0, 0]

        return [total_disponible, porcentaje, bar_color]

    @property
    def disponibleGasoil(self):

        porcentaje = 0
        bar_color = 1

        total = Combustible.objects.filter(estacion_id=self.id, tipo_combustible='Gasoil').aggregate(Sum('cantidad'))
        total_cargado = Carga.objects.filter(estacion_id=self.id, tipo_combustible='Gasoil').aggregate(Sum('cantidad'))

        if total_cargado['cantidad__sum'] is None:
            tc = float(0.0)
        else:
            tc = total_cargado['cantidad__sum']

        if total['cantidad__sum']:
            total_publico = total['cantidad__sum'] - self.reserva_gasoil
            total_disponible = total_publico - tc
            porcentaje = (total_disponible / total_publico) * 100
            if porcentaje < 25:
                bar_color = 1
            elif 25 <= porcentaje <= 50:
                bar_color = 2
            elif porcentaje > 50:
                bar_color = 3
        else:
            return [0, 0, 0]

        return [total_disponible, porcentaje, bar_color]


class Combustible(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    tipo_combustible = models.CharField(max_length=10, choices=COMBUSTIBLE_TIPO_CHOICES)
    cantidad = models.FloatField(default=0)
    fecha_carga = models.DateField()

    created_by = UserForeignKey(auto_user_add=True, related_name='combustible_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='combustible_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.tipo_combustible)


class Vehiculo(models.Model):
    placa = models.CharField(max_length=7, primary_key=True)
    cilindros = models.CharField(max_length=10, choices=CILINDROS_CHOICES, default='4')

    created_by = UserForeignKey(auto_user_add=True, related_name='vehiculos_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='vehiculos_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.placa


class Carga(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_combustible = models.CharField(max_length=10, choices=COMBUSTIBLE_TIPO_CHOICES)
    cantidad = models.FloatField(default=0)

    created_by = UserForeignKey(auto_user_add=True, related_name='carga_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='carga_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.vehiculo.placa)
