from django.contrib import admin

from .models import Estacion, Combustible, Vehiculo, Carga, Cola, VehiculoResumen, \
    Rebotado, Contador, ColaConsulta, RebotadoBloqueado


class ContadorInline(admin.TabularInline):
    model = Contador
    #fields = ['resumen',]


@admin.register(Estacion)
class EstacionAdmin(admin.ModelAdmin):
    pass
    inlines = [ContadorInline]
    #list_display = ('cedula','primer_apellido', 'primer_nombre')
    #search_fields = ['cedula', 'primer_apellido']


@admin.register(Contador)
class ContadorAdmin(admin.ModelAdmin):
    pass


@admin.register(Combustible)
class CombustibleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Planificacion', {'fields': ('estacion', 'estado', 'litros_planeados_g91', 'litros_planeados_g95', 'litros_planeados_gsl', 'fecha_planificacion', 'apertura', 'completado', 'nota'), 'classes': ['wide']}),
        ('Reporte', {'fields': ('litros_surtidos_g91', 'litros_surtidos_g95', 'litros_surtidos_gsl', 'notas',), 'classes': ['wide']}),
    )
    list_display = ('estacion', 'estado','nota', 'fecha_planificacion', 'apertura', 'completado', 'litros_planeados_g91', 'litros_planeados_g95', 'litros_planeados_gsl', 'litros_surtidos_g91', 'litros_surtidos_g95', 'litros_surtidos_gsl')
    list_filter = ('estacion',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Datos Generales', {'fields': ('placa', 'cedula', 'tipo_vehiculo', 'cilindros', 'organizacion', 'paso_preferencial',), 'classes': ['wide']}),
        ('Multa', {'fields': ('bloqueado', 'bloqueado_motivo', 'bloqueado_fecha', 'bloqueado_hasta',), 'classes': ['wide']}),
    )
    list_display = ('placa', 'cedula', 'usuario', 'bloqueado', 'tipo_vehiculo')
    search_fields = ['placa', 'cedula']
    list_filter = ('tipo_vehiculo',)
    readonly_fields = ('usuario',)


@admin.register(Rebotado)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('combustible', 'vehiculo', 'created_at', 'created_by')
    search_fields = ['vehiculo__placa']
    exclude = ['usuario']
    #list_filter = ('combustible',)


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


@admin.register(Cola)
class ColaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'combustible', 'cargado', 'cantidad', 'cedula', 'nota', 'created_by','created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]
    #list_filter = ('combustible',)


@admin.register(ColaConsulta)
class ColaConsultaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vehiculo', 'created_by','created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]


@admin.register(RebotadoBloqueado)
class RebotadoBloqueado(admin.ModelAdmin):
    list_display = ('vehiculo', 'combustible', 'created_by', 'created_at', 'last_modified_at')
    search_fields = ['vehiculo__placa',]
