from rest_framework import viewsets
from dgas.gas_app.serializer import CargaSerializer, VehiculoSerializer
from rest_framework.permissions import IsAuthenticated
from dgas.gas_app.models import Vehiculo, Carga
from rest_framework.decorators import detail_route
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
import json


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

    @detail_route()
    def ultima_carga(self, request, vehiculo=None):
        carga = self.Carga.objects.filter(vehiculo=vehiculo).latest('created_at')
        return Response(carga.data)


class UltimaCargaList(APIView):
    serializer_class = CargaSerializer

    def get(self, request, *args, **kwargs):
        """
        Para el chequeo de cargas a un dia
        """
        from datetime import datetime, timedelta
        import pytz
        utc = pytz.UTC

        hoy = datetime.now()

        placa = self.kwargs['placa']

        try:

            ultima_carga = Carga.objects.filter(vehiculo=placa).latest('created_at')

            p = ultima_carga.created_at + timedelta(days=2)
            print(p, hoy)

            hoy = hoy.replace(tzinfo=utc)
            u = ultima_carga.created_at.replace(tzinfo=utc)

            print(ultima_carga.estacion, ultima_carga.created_at, hoy)
            if p > hoy:
                uc = json.dumps({"cargar": "false", "estacion": str(ultima_carga.estacion), "created_at": str(ultima_carga.created_at)})
            else:
                uc = json.dumps({"cargar": "true"})

        except Carga.DoesNotExist:
            uc = json.dumps({"cargar": "true"})

        return Response(uc)
