from django.urls import path, include

from dgas.supervisor_app.views import supervisor_vehiculos
from dgas.supervisor_app.views import estadisticas

import dgas.supervisor_app.dash_app

app_name = "supervisor_app"

urlpatterns = [

    #path('', public_base.Publico.as_view(), name='estaciones'),
    path('vehiculos/', supervisor_vehiculos.SupervisorVehiculo.as_view(), name='supervisor_vehiculos'),
    #path('estaciones_mapa/', public_base.EstacionesMapa.as_view(), name='estaciones_mapa'),
    #path('colas/', public_base.ColasTemplateView.as_view(), name='colas'),
    path('estadistica/', estadisticas.SupervisorEstadisticas.as_view(), name='supervisor_estadistica'),
    path('estadistica/plots/', estadisticas.SupervisorPlots.as_view(), name='supervisor_plots'),
    path('estadistica/dash/', estadisticas.SupervisorDashPoltly.as_view(), name='supervisor_dash_plotly'),

]
