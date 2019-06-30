from django.urls import path

from dgas.public_app.views import public_base
from dgas.public_app.views import vehiculos

app_name = "public_app"

urlpatterns = [

    path('', public_base.Publico.as_view(), name='estaciones'),
    path('estaciones/', public_base.Estaciones.as_view(), name='estaciones'),
    path('colas/', public_base.ColasTemplateView.as_view(), name='colas'),
    path('colas-historico/', public_base.ColasHistorioTemplateView.as_view(), name='colas-historico'),

    path('vehiculos/', vehiculos.VehiculoListView.as_view(), name='vehiculos_list'),
    path('vehiculos/create', vehiculos.VehiculoCreateView.as_view(), name='vehiculo_create'),
    path('vehiculos/update/<str:placa>', vehiculos.VehiculoUpdateView.as_view(), name='vehiculo_update'),




]
