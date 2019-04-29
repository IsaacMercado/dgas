from django.db import models
from model_utils import Choices


COMBUSTIBLE_TIPO_CHOICES = Choices('91', '95', 'Gasoil')
CILINDROS_CHOICES = Choices('1', '4', '6', '8')


class Estacion(models.Model):
    opetativa = models.BooleanField(default=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


class Combustible(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    tipo_combustible = models.CharField(max_length=10, choices=COMBUSTIBLE_TIPO_CHOICES, default='91')
    cantidad = models.FloatField(default=0)
    fecha_carga = models.DateField()


class Vehiculo(models.Model):
    placa = models.CharField(max_length=7, db_index=True)
    cilindros = models.CharField(max_length=10, choices=CILINDROS_CHOICES, default='4')


class Carga(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)

