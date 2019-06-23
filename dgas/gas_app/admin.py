from django.contrib import admin

from .models import Estacion, Combustible, Vehiculo, Carga, Cola


class CombustibleInline(admin.TabularInline):
    model = Combustible
    #fields = ['resumen',]


@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    inlines = [CombustibleInline]
    #list_display = ('cedula','primer_apellido', 'primer_nombre')
    #search_fields = ['cedula', 'primer_apellido']


@admin.register(Combustible)
class CombustibleAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'tipo_combustible', 'estado', 'cantidad', 'completado')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'cedula', 'tipo_vehiculo')
    search_fields = ['placa', 'cedula' ]


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'tipo_combustible', 'cantidad', 'created_by', 'created_at')


@admin.register(Cola)
class ColaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'cargado', 'cantidad', 'created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]
