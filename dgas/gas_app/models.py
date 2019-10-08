from django.db import models
from model_utils import Choices
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models import Sum
from dgas.users.models import GasUser, User, Municipio

COMBUSTIBLE_TIPO_CHOICES = Choices('91', '95', 'Gasoil')
CILINDROS_CHOICES = Choices('1', '2', '3', '4', '6', '8')
CARGA_ESTADO_CHOICES = Choices('En plan', 'En camino', 'Descargando', 'Despachando', 'Cerrada')
MUNICIPIOS_CHOICES = Choices('Libertador', 'Campo Elias', 'Sucre', 'Santos Marquina', 'Alberto Adriani')
TIPO_VEHICULO_CHOICES = Choices(
    'Particular',
    'TP Gasolina',
    'TP Gasoil',
    'Oficial Diario',
    'Oficial Interdiario',
    'Moto',
    'Moto Taxita',
    'Taxi',
    'Carga'
)


class Estacion(models.Model):
    #usuario = models.ForeignKey(GasUser, on_delete=models.CASCADE, blank=True, null=True)
    codigo_cliente = models.PositiveIntegerField(default=0)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    municipio_estacion = models.ForeignKey(Municipio, on_delete=models.CASCADE, default=15, null=True, blank=True)
    municipio = models.CharField(max_length=20, choices=MUNICIPIOS_CHOICES, default='Libertador')
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
        return ('%s') % (self.nombre,)

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


class Contador(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='estaciones_islas', default=1)
    nombre = models.CharField(max_length=20, default='')
    tipo_combustible = models.CharField(max_length=10, choices=COMBUSTIBLE_TIPO_CHOICES, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return ('%s, %s') % (self.nombre, self.tipo_combustible,)


class ContadorMedida(models.Model):
    contador = models.ForeignKey(Contador, on_delete=models.CASCADE, related_name='_islas', default=1)
    cantidad = models.PositiveIntegerField(default=0)

    created_by = UserForeignKey(auto_user_add=True, related_name='contador_medida')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='contador_medida_update')
    last_modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('%s, %s') % (self.nombre, self.tipo_combustible,)


class Combustible(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=CARGA_ESTADO_CHOICES, default='En Camino')
    nota = models.CharField(max_length=100, blank=True, null=True)
    fecha_planificacion = models.DateField(null=True, blank=True)
    fecha_apertura = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    apertura = models.BooleanField(default=False)
    completado = models.BooleanField(default=False)

    litros_surtidos_g91 = models.PositiveIntegerField(default=0)
    litros_surtidos_g95 = models.PositiveIntegerField(default=0)
    litros_surtidos_gsl = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True, null=True)

    created_by = UserForeignKey(auto_user_add=True, related_name='combustible_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='combustible_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.estacion.nombre)


class Vehiculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    placa = models.CharField(max_length=7, primary_key=True, help_text='Sin espacio en blanco y letras en mayusculas')
    cedula = models.CharField('Nro. de cédula de identidad', max_length=20, default='No Registrado', help_text='Indicar el numero de cedula que aparece en el carnet de circulación vial')
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES, default='Particular')
    cilindros = models.CharField(max_length=10, choices=CILINDROS_CHOICES, default='4')
    organizacion = models.CharField('Organización', max_length=100, default='No aplica')
    paso_preferencial = models.BooleanField(default=False)

    bloqueado = models.BooleanField(default=False)
    bloqueado_motivo = models.TextField(blank=True, null=True)
    bloqueado_fecha = models.DateTimeField(blank=True, null=True)
    bloqueado_hasta = models.DateField(blank=True, null=True)

    created_by = UserForeignKey(auto_user_add=True, related_name='vehiculos_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='vehiculos_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.placa


class VehiculoResumen(Vehiculo):
    class Meta:
        proxy = True
        verbose_name = "Vehiculo Resumen"
        verbose_name_plural = "Vehiculo Resumen"

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


class Cola(models.Model):
    combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE, related_name='colas')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    tipo_combustible = models.CharField(max_length=10, choices=COMBUSTIBLE_TIPO_CHOICES, default=95, null=True, blank=True)
    cantidad = models.FloatField(default=0)
    cargado = models.BooleanField(default=False)

    created_by = UserForeignKey(auto_user_add=True, related_name='cola_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='cola_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-last_modified_at',)
        unique_together = ('vehiculo', 'combustible',)

    def __str__(self):
        return str(self.vehiculo.placa)


class ColaConsulta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    created_by = UserForeignKey(auto_user_add=True, related_name='cola_consulta_created')
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='cola_consula_updated')
    last_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-last_modified_at',)

    def __str__(self):
        return str(self.vehiculo.placa)


class Rebotado(models.Model):
    combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE, related_name='rebotados')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='rebotados_created')
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='rebotados_updated')

    def __str__(self):
        return str(self.vehiculo.placa)


