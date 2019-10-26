from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, VehiculoUserViewSet, VehiculoSupervisorViewSet, \
    CargaViewSet, UltimaCargaList, \
    CombustibleViewSet, ColaViewSet, UltimaColaList, \
    ContarCola, ColaCrudViewSet, ColaPublicaViewSet, ColaPublicaHistoricaViewSet, \
    ColaPublicaHistoricaViewSet, EstacionViewSet, CombustibleHistoricoViewSet, BuscarPlacaPubico, \
    RebotadoViewSet, RebotadoBloqueadoViewSet, ConsultarVehiculo, CombustiblePublicoViewSet, \
    EstacionPublicViewSet, VehiculoBloqueadosViewSet

from dgas.gas_app import views

app_name = "api"

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'vehiculos_user', VehiculoUserViewSet)
router.register(r'vehiculos_rebotados', RebotadoViewSet)
router.register(r'vehiculos_multados', VehiculoBloqueadosViewSet)
router.register(r'vehiculos_rebotados_bloqueado', RebotadoBloqueadoViewSet)

router.register(r'vehiculos_supervisor', VehiculoSupervisorViewSet)

router.register(r'cargas', CargaViewSet)
router.register(r'combustible', CombustibleViewSet)
router.register(r'cola/(?P<combustible_id>\d+)', ColaViewSet)
router.register(r'cola-crud/(?P<combustible_id>\d+)', ColaCrudViewSet)
#public
router.register(r'estaciones', EstacionViewSet)
router.register(r'combustible_publico', CombustiblePublicoViewSet)
router.register(r'estaciones_publico', EstacionPublicViewSet)
router.register(r'combustible_historico', CombustibleHistoricoViewSet)
router.register(r'colas_publico/(?P<combustible_id>\d+)', ColaPublicaViewSet)
router.register(r'colas_historico/(?P<combustible_id>\d+)', ColaPublicaHistoricaViewSet)



urlpatterns = [

    path("", include(router.urls)),
    path('ultima_carga/<str:placa>', UltimaCargaList.as_view()),
    path('ultima_cola/<str:placa>', UltimaColaList.as_view()),
    path('cola/contar_cola/<int:combustible_id>', ContarCola.as_view()),
    path('consultar_vehiculo/<str:placa>', ConsultarVehiculo.as_view()),

    # Recolector
    path('buscar_placa_publico/<str:placa>', BuscarPlacaPubico.as_view()),

    #path('c/clientes/detail/<int:pk>', clientesa.ClienteDetailView.as_view(), name='cliente_detail'),
    #path('c/clientes/delete/<int:pk>', clientesa.ClienteDeleteView.as_view(), name='cliente_delete'),

]
