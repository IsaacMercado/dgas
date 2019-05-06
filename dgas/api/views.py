from rest_framework import viewsets
from dgas.gas_app.serializer import CargaSerializer, VehiculoSerializer
from rest_framework.permissions import IsAuthenticated
from dgas.gas_app.models import Vehiculo, Carga


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Vehiculos
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    #permission_classes = (IsAuthenticated,)


class CargaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Cargas
    """
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    #permission_classes = (IsAuthenticated,)
