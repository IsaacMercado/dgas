from django.urls import path

from dgas.public_app.views import public_base

app_name = "public_app"

urlpatterns = [

    path('', public_base.Publico.as_view(), name='estaciones'),
    path('estaciones/', public_base.Estaciones.as_view(), name='estaciones'),
    path('colas/', public_base.ColasTemplateView.as_view(), name='colas'),
    path('colas-historico/', public_base.ColasHistorioTemplateView.as_view(), name='colas-historico'),

]
