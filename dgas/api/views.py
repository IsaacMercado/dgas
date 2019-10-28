import json
from django.core import serializers
from django.db.models import Count, Sum, Subquery, IntegerField
from rest_framework import generics
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.decorators import detail_route
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta, date
import pytz
from django.core.serializers.json import DjangoJSONEncoder

from dgas.gas_app.models import Vehiculo, Carga, Cola, Combustible, Estacion, Rebotado, RebotadoBloqueado, ColaConsulta
from dgas.gas_app.serializer import CargaSerializer, VehiculoSerializer, VehiculoUserSerializer, \
    CombustibleSerializer, ColaSerializer, VehiculoSupervisorSerializer, \
    ColaCrudSerializer, EstacionSerializer, ColaPublicoSerializer, RebotadoSerializer, RebotadoBloqueadoSerializer, \
    VehiculoBloqueadosSerializer
from dgas.users.models import User


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Vehiculos
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    # permission_classes = (IsAuthenticated,)


class VehiculoSupervisorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Vehiculos
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSupervisorSerializer
    # permission_classes = (IsAuthenticated,)


class VehiculoUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Vehiculos
    """
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoUserSerializer

    def post_save(self, obj):
        obj.usuario = self.request.user


class VehiculoBloqueadosViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoBloqueadosSerializer

    def get_queryset(self):

        qs = self.queryset.filter(bloqueado=True)

        return qs



class RebotadoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Rebotado
    """
    queryset = Rebotado.objects.all()
    serializer_class = RebotadoSerializer


class RebotadoBloqueadoViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Rebotado
    """
    queryset = RebotadoBloqueado.objects.all()
    serializer_class = RebotadoBloqueadoSerializer


class CargaViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Cargas
    """
    queryset = Carga.objects.all()
    serializer_class = CargaSerializer

    # permission_classes = (IsAuthenticated,)

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

            p = ultima_carga.created_at + timedelta(days=5)
            print(p, hoy)

            hoy = hoy.replace(tzinfo=utc)
            u = ultima_carga.created_at.replace(tzinfo=utc)

            print(ultima_carga.estacion, ultima_carga.created_at, hoy)
            if p.date() > hoy.date():
                uc = json.dumps({"cargar": "false", "estacion": str(ultima_carga.estacion),
                                 "created_at": str(ultima_carga.created_at)})
            else:
                uc = json.dumps({"cargar": "true"})

        except Carga.DoesNotExist:
            uc = json.dumps({"cargar": "true"})

        return Response(uc)


class UltimaColaList(APIView):
    serializer_class = ColaSerializer

    def get(self, request, *args, **kwargs):
        """
        Para el chequeo de cargas
        """
        utc = pytz.UTC

        hoy = date.today()

        placa = self.kwargs['placa']

        try:
            vehiculo = Vehiculo.objects.get(placa=placa)

            if not vehiculo.bloqueado:

                if vehiculo.tipo_vehiculo == "Moto Taxita" or vehiculo.tipo_vehiculo == "Oficial Interdiario":
                    frecuencia_de_carga = 2

                elif vehiculo.tipo_vehiculo == "Oficial Diario" or vehiculo.tipo_vehiculo == "TP Gasolina" or vehiculo.tipo_vehiculo == "TP Gasoil":
                    frecuencia_de_carga = 1
                else:
                    frecuencia_de_carga = 4

                try:

                    ultima_cola = Cola.objects.filter(vehiculo=placa).latest('created_at')

                    # h4 = timedelta(hours=4)

                    ultima_carga = ultima_cola.created_at
                    ultima_carga_h4 = ultima_carga - timedelta(hours=4)
                    proxima_carga = ultima_carga_h4 + timedelta(days=frecuencia_de_carga)
                    proxima_carga = proxima_carga.date()
                    p = proxima_carga

                    print('##### ultima carga', ultima_carga_h4.date(), p, hoy)

                    if not ultima_cola.cargado:
                        uc = json.dumps({"cargar": "false",
                                         "bloqueado": "false",
                                         "mensaje": " ya esta registrado para surtir gasolina",
                                         "estacion": str(ultima_cola.combustible),
                                         "proxima_recarga": "",
                                         "created_at": str(ultima_cola.created_at)})
                    elif p > hoy:
                        uc = json.dumps({"cargar": "false", "mensaje": " ya surtio gasolina",
                                         "bloqueado": "false",
                                         "estacion": str(ultima_cola.combustible),
                                         "proxima_recarga": str(p),
                                         "created_at": str(ultima_cola.created_at)})
                    else:
                        uc = json.dumps({"cargar": "true"})

                except Cola.DoesNotExist:
                    uc = json.dumps({"cargar": "true"})
            else:
                uc = json.dumps(
                    {
                        "bloqueado": "true",
                        "bloqueado_fecha": str(vehiculo.bloqueado_fecha),
                        "bloqueado_hasta": str(vehiculo.bloqueado_hasta),
                        "bloqueado_motivo": vehiculo.bloqueado_motivo
                    }
                )

        except Vehiculo.DoesNotExist:
            uc = json.dumps({"error": "true", "msg": "Ocurrio un error, por favor intente de nuevo"})

        return Response(uc)


'''
class CombustibleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Combustible.objects.all()
    serializer_class = CombustibleSerializer
    #permission_classes = (AllowAny,)
'''

class CombustibleViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Combustible.objects.all()
    serializer_class = CombustibleSerializer
    #permission_classes = (AllowAny,)

    '''
    total_surtidos = self.queryset.annotate(total_surtidos=Sum('colas__cantidad'))
    total_cola = self.queryset.annotate(Count('colas', distinct=True))
    total_rebotados = self.queryset.annotate(Count('rebotados', distinct=True))

    qs = self.queryset.filter(completado=True) \
        .annotate(
        total_cola=Subquery(total_cola.values('cola'), output_field=IntegerField()),
        total_rebotados=Subquery(total_rebotados.values('rebotados'), output_field=IntegerField()),
        total_surtidos=Subquery(total_surtidos.values('total_surtidos'), output_field=IntegerField())
    )
    '''

    def get_queryset(self):
        qs = self.queryset.filter(completado=False)\
            .exclude(estado='En plan',)\
            .annotate(
            total_cola=Count('colas', distinct=True),
            total_rebotados=Count('rebotados', distinct=True),
            total_surtidos=Sum('colas__cantidad', distinct=True)
        )

        return qs


class CombustiblePublicoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Combustible.objects.all()
    serializer_class = CombustibleSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):

        if self.request.GET.get('q'):
            today = date.today() + timedelta(days=1)
        else:
            today = date.today()

        qs = self.queryset.filter(fecha_planificacion=today)

        return qs


class CombustibleHistoricoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Combustible.objects.all()
    serializer_class = CombustibleSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        #qs = self.queryset.filter(completado=True).annotate(total_cola=Count('colas'))

        qs = self.queryset.filter(completado=True) \
            .annotate(
            total_cola=Count('colas', distinct=True),
            total_rebotados=Count('rebotados', distinct=True),
            total_surtidos=Sum('colas__cantidad', distinct=True)
        )

        return qs


'''
mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
'''


class ColaPublicaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cola.objects.all()
    serializer_class = ColaPublicoSerializer

    permission_classes = (AllowAny,)

    def get_queryset(self):
        combustible_id = self.kwargs['combustible_id']
        qs = self.queryset.filter(combustible_id=combustible_id, cargado=False)
        return qs


class ColaPublicaHistoricaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Cola.objects.all()
    serializer_class = ColaPublicoSerializer

    permission_classes = (AllowAny,)

    def get_queryset(self):
        combustible_id = self.kwargs['combustible_id']
        qs = self.queryset.filter(combustible_id=combustible_id)
        return qs


class ColaCrudViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Cola.objects.all()
    serializer_class = ColaCrudSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        combustible_id = self.kwargs['combustible_id']
        qs = self.queryset.filter(combustible_id=combustible_id, cargado=False)
        return qs


class ColaViewSet(viewsets.ModelViewSet):
    queryset = Cola.objects.all()
    serializer_class = ColaSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        combustible_id = self.kwargs['combustible_id']
        qs = self.queryset.filter(combustible_id=combustible_id, cargado=False)
        return qs

    # @action(detail=False, url_path='ver-aja', url_name='ver_aja',)
    @action(detail=False)
    def set_aja(self):
        content = {'total': 0}
        return Response(content)

    @action(detail=True)
    def count(self):
        # combustible_id = self.kwargs['combustible_id']
        # cargado = self.objects.annotate(total_cargado=Count('cargado'))
        # print(cargado)
        # queryset = self.filter_queryset(self.get_queryset())
        # count = queryset.count()

        # por_cargar = count - cargado[0].total_cargado

        # content = {'total': count, 'cargado': cargado[0].total_cargado, 'por_cargar': por_cargar}
        content = {'total': 0, 'cargado': 0, 'por_cargar': 0}
        return Response(content)

    @detail_route()
    def ultima_cola(self, request, vehiculo=None):
        cola = self.Cola.objects.filter(vehiculo=vehiculo).latest('created_at')
        return Response(cola.data)


class ContarCola(APIView):
    queryset = Cola.objects.all()

    def get(self, request, *args, **kwargs):

        combustible_id = self.kwargs['combustible_id']

        combustible = Combustible.objects.get(pk=combustible_id)

        cargado = Cola.objects.filter(combustible_id=combustible_id, cargado=True).count()
        total = Cola.objects.filter(combustible_id=combustible_id).count()
        total_rebotados = Rebotado.objects.filter(combustible_id=combustible_id).count()

        if total and cargado:
            por_cargar = total - cargado

            content = {
                'total': total,
                'cargado': cargado,
                'por_cargar': por_cargar,
                'estado': combustible.estado,
                'estacion': combustible.estacion.nombre,
                'total_rebotados': total_rebotados,
            }

            print(content)

        else:
            content = {
                'total': 0,
                'cargado': 0,
                'por_cargar': 0,
                'estado': combustible.estado,
                'estacion': combustible.estacion.nombre,
                'total_rebotados': total_rebotados,
            }
        return Response(content)


class EstacionViewSet(viewsets.ModelViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer


class EstacionPublicViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Estacion.objects.all()
    serializer_class = EstacionSerializer
    permission_classes = (AllowAny,)


class BuscarPlacaPubico(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = ColaSerializer
    # permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        Para el chequeo de cargas a un dia
        """
        from datetime import datetime, timedelta, date
        import pytz
        utc = pytz.UTC

        hoy = date.today()

        placa = self.kwargs['placa']

        frecuencia_de_carga = 0
        en_peril = False

        try:

            vehiculo = Vehiculo.objects.get(placa=placa)

            if vehiculo.usuario is None:
                en_peril = False
            else:
                u = User.objects.get(pk=vehiculo.usuario.id)
                if u.id == request.user.id:
                    en_peril = True
                    vc = ColaConsulta(usuario_id=u.id, vehiculo_id=vehiculo.placa)
                    vc.save()

            if vehiculo.tipo_vehiculo == "Moto Taxita" or vehiculo.tipo_vehiculo == "Oficial Interdiario":
                frecuencia_de_carga = 2

            elif vehiculo.tipo_vehiculo == "Oficial Diario" or vehiculo.tipo_vehiculo == "TP Gasolina" or vehiculo.tipo_vehiculo == "TP Gasoil":
                frecuencia_de_carga = 1
            else:
                    frecuencia_de_carga = 4

        except Vehiculo.DoesNotExist:
            frecuencia_de_carga = 4

        if en_peril:

            try:

                ultima_cola = Cola.objects.filter(vehiculo=placa).latest('created_at')

                ultima_carga = ultima_cola.created_at
                ultima_carga_h4 = ultima_carga - timedelta(hours=4)
                proxima_carga = ultima_carga_h4 + timedelta(days=frecuencia_de_carga)
                proxima_carga = proxima_carga.date()
                # p = proxima_carga.replace(hour=0, minute=0, second=0, microsecond=0)
                p = proxima_carga

                if not ultima_cola.cargado:
                    uc = json.dumps({"cargar": "false",
                                     "mensaje": " ya esta registrado para surtir gasolina",
                                     "estacion": str(ultima_cola.combustible),
                                     "proxima_recarga": "",
                                     "created_at": str(ultima_cola.created_at)})
                elif p >= hoy:
                    uc = json.dumps({"cargar": "false", "mensaje": " ya surtio gasolina",
                                     "estacion": str(ultima_cola.combustible),
                                     "proxima_recarga": str(p),
                                     "created_at": str(ultima_cola.created_at)})
                else:
                    uc = json.dumps({"cargar": "true",
                                     "mensaje": " vehiculo puede surtir gasolina",
                                     "estacion": str(ultima_cola.combustible),
                                     "proxima_recarga": "",
                                     "created_at": str(ultima_cola.created_at)})

            except Cola.DoesNotExist:
                uc = json.dumps({"cargar": "true",
                                 "mensaje": " puede surtir gasolina",
                                 "estacion": "",
                                 "proxima_recarga": "",
                                 "created_at": ''})
        else:

            uc = json.dumps({"cargar": "true",
                             "mensaje": "no_perfil",
                             "estacion": "",
                             "proxima_recarga": "",
                             "created_at": ''})

        return Response(uc)


class ConsultarVehiculo(mixins.ListModelMixin, generics.GenericAPIView):

    serializer_class = ColaSerializer
    # permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        Para el chequeo de cargas a un dia
        """
        from datetime import datetime, timedelta, date
        import pytz
        utc = pytz.UTC

        hoy = date.today()

        placa = self.kwargs['placa']

        try:

            vehiculo = Vehiculo.objects.get(placa=placa)

            colas = Cola.objects.filter(vehiculo=placa).values('combustible__estacion__nombre', 'created_at').order_by('-created_at')[:3]
            rebotes = Rebotado.objects.filter(vehiculo=placa).values('combustible__estacion__nombre', 'created_at').order_by('-created_at')[:3]

            colas_q = json.dumps(list(colas), cls=DjangoJSONEncoder)
            rebotes_q = json.dumps(list(rebotes), cls=DjangoJSONEncoder)

            uc = json.dumps(
                {
                    "existe": "true",
                    "placa": vehiculo.placa,
                    "organizacion": vehiculo.organizacion,
                    "paso_preferencial": vehiculo.paso_preferencial,
                    "bloqueado": vehiculo.bloqueado,
                    "bloqueado_motivo": vehiculo.bloqueado_motivo,
                    "bloqueado_hasta": str(vehiculo.bloqueado_hasta),
                    "tipo_vehiculo": vehiculo.tipo_vehiculo,
                    "colas": colas_q,
                    "rebotes": rebotes_q

                }
            )

        except Vehiculo.DoesNotExist:

            uc = json.dumps(
                {
                    "existe": "false",
                }
            )

        return Response(uc)

