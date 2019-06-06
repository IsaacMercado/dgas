from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, CargaViewSet, UltimaCargaList

from dgas.gas_app import views

app_name = "api"

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'cargas', CargaViewSet)

urlpatterns = [

    path("", include(router.urls)),
    path('ultima_carga/<str:placa>', UltimaCargaList.as_view()),

    # Recolector

    #path('c/clientes/detail/<int:pk>', clientesa.ClienteDetailView.as_view(), name='cliente_detail'),
    #path('c/clientes/delete/<int:pk>', clientesa.ClienteDeleteView.as_view(), name='cliente_delete'),

]
