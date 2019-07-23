# coding=utf-8
import time
import datetime

from django.core.management.base import BaseCommand
from dateutil import relativedelta

from dgas.gas_app.models import Carga, Cola


class Command(BaseCommand):

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument('--export',
                            dest='export',
                            default=False,
                            help='Export carga to CSV')

        #parser.add_argument('fecha')
        #parser.add_argument('estacion')

    def handle(self, *args, **options):
        # ...
        if options['export']:
            """
            Comando para verificar vacaciones de empleados
            
            from pytz import timezone
            from django.db.models import Count
            from django.db.models import Q

            #print('Verificando')

            estacion = options['estacion']
            fecha = options['fecha']
            fecha_d = fecha + ' 00:00:00'
            fecha_h = fecha + ' 23:59:59'
            desde = datetime.datetime.strptime(fecha_d, "%Y-%m-%d %H:%M:%S")
            hasta = datetime.datetime.strptime(fecha_h, "%Y-%m-%d %H:%M:%S")

            cargas = Carga.objects.filter(estacion_id=estacion, created_at__gte=desde, created_at__lte=hasta).order_by('-created_at')

            for carga in cargas:
                if carga.cantidad > 42:
                    print(carga.vehiculo_id+'|'+str(carga.cantidad)+'|'+str(carga.created_at))
            """

            estacion = [50, 57, 69, 83, 99, 114, 129, 147, 165, 185, 212, 230, 247]

            cola = Cola.objects.filter(combustible_id__in=estacion)

            for c in cola:
                print(c.vehiculo, c.combustible)
