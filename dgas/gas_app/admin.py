from django.contrib import admin

from .models import Estacion, Combustible, Vehiculo, Carga, Cola, VehiculoResumen, \
    Rebotado, Pico, ColaConsulta


class PicoInline(admin.TabularInline):
    model = Pico
    #fields = ['resumen',]


@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    pass
    inlines = [PicoInline]
    #list_display = ('cedula','primer_apellido', 'primer_nombre')
    #search_fields = ['cedula', 'primer_apellido']


@admin.register(Pico)
class PicoAdmin(admin.ModelAdmin):
    pass


@admin.register(Combustible)
class CombustibleAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'tipo_combustible', 'estado', 'cantidad', 'completado')
    list_filter = ('estacion',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'cedula', 'usuario', 'tipo_vehiculo')
    search_fields = ['placa', 'cedula']
    list_filter = ('tipo_vehiculo',)


@admin.register(Rebotado)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('combustible', 'vehiculo', 'created_at', 'created_by')
    search_fields = ['vehiculo__placa']
    #list_filter = ('tipo_vehiculo',)


@admin.register(VehiculoResumen)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'gas_app/admin/vehiculo_resumen_change_list.html'
    #date_hierarchy = 'created'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'total': Count('id'),
        'total_sales': Sum('price'),
        }
        response.context_data['resumen'] = list(
            qs
            .values('sale__category__name')
            .annotate(**metrics)
            .order_by('-total_sales')
        )

        return response


@admin.register(Carga)
class CargaAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'tipo_combustible', 'cantidad', 'created_by', 'created_at')


@admin.register(Cola)
class ColaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'combustible', 'cargado', 'cantidad', 'created_by','created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]


@admin.register(ColaConsulta)
class ColaConsultaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vehiculo', 'created_by','created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]
