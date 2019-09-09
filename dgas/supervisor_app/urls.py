from django.urls import path

from dgas.supervisor_app.views import supervisor_vehiculos

app_name = "supervisor_app"

urlpatterns = [

    #path('', public_base.Publico.as_view(), name='estaciones'),
    path('vehiculos/', supervisor_vehiculos.SupervisorVehiculo.as_view(), name='supervisor_vehiculos'),
    #path('estaciones_mapa/', public_base.EstacionesMapa.as_view(), name='estaciones_mapa'),
    #path('colas/', public_base.ColasTemplateView.as_view(), name='colas'),

]
