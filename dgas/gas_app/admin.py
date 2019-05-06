from django.contrib import admin

from .models import Estacion, Combustible, Vehiculo, Carga


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
    pass


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    pass


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'tipo_combustible', 'cantidad', 'created_by', 'created_at')
