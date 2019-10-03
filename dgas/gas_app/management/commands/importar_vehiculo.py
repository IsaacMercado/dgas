# coding=utf-8
import string
import traceback

from django.core.management.base import BaseCommand
from dgas.gas_app.models import Vehiculo, Cola
import datetime


class Command(BaseCommand):

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
                '--cargar_vehiculos',
            action='store_true',
            dest='cargar_vehiculos',
            default=False,
            help='Carga los vehiculos'
        )

        # Named (optional) arguments
        parser.add_argument(
            '--cargar_moto_taxi',
            action='store_true',
            dest='cargar_moto_taxi',
            default=False,
            help='Carga moto taxita'
        )

        parser.add_argument(
            '--cargar_transporte_publico',
            action='store_true',
            dest='cargar_transporte_publico',
            default=False,
            help='Carga transporte publico'
        )

        parser.add_argument(
            '--cargar_transporte_publico_gasoil',
            action='store_true',
            dest='cargar_transporte_publico_gasoil',
            default=False,
            help='Carga transporte publico gasoil'
        )

        parser.add_argument(
            '--cargar_oficial_diario',
            action='store_true',
            dest='cargar_oficial_diario',
            default=False,
            help='Cargar oficial diario'
        )

        parser.add_argument(
            '--cola_verifica',
            action='store_true',
            dest='cola_verifica',
            default=False,
            help='Verificar archivo de cola'
        )

        parser.add_argument(
            '--cola_carga',
            action='store_true',
            dest='cola_carga',
            default=False,
            help='Carga archivo de cola'
        )

        parser.add_argument('archivo')

    def handle(self, *args, **options):

        if options['cargar_vehiculos']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            for file_line in file_list:

                try:
                    [placa, cedula, cilindros] = file_line.split(",")
                    cilindros = cilindros.strip(' \t\n\r')
                    print(placa, cedula, cilindros)
                except:
                   pass

                try:
                    ta = Vehiculo(placa=placa,cedula=cedula, tipo_vehiculo='Moto', cilindros=cilindros)
                    ta.save()
                except:
                    print("Placa: " + placa +"Ya esta rgistrada")

        if options['cargar_moto_taxi']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0

            for file_line in file_list:
                nro_linea += 1
                try:
                    [placa, cedula] = file_line.split(",")
                    cedula = cedula.strip(' \t\n\r')
                    print(placa, cedula)
                except:
                   print('Error leyendo Linea nro: '+str(nro_linea))
                   print(file_line)
                   exit(0)

                try:
                    ta = Vehiculo.objects.get(placa=placa)
                    ta.tipo_vehiculo="Moto Taxita"
                    ta.cedula=cedula
                    ta.save()
                except:
                    print("Placa: " + placa +"Ya no esta registrada")
                    mt_insert = Vehiculo(placa=placa, cedula=cedula, tipo_vehiculo='Moto Taxita', cilindros=1)
                    mt_insert.save()

        if options['cargar_transporte_publico']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0

            for file_line in file_list:
                nro_linea += 1
                try:
                    [placa] = file_line.split(",")
                    placa = placa.strip(' \t\n\r')
                    print(placa)
                except:
                   print('Error leyendo Linea nro: '+str(nro_linea))
                   print(file_line)
                   exit(0)

                try:
                    ta = Vehiculo.objects.get(placa=placa)
                    ta.tipo_vehiculo="TP Gasolina"
                    ta.save()
                except:
                    nv = Vehiculo(placa=placa, tipo_vehiculo="TP Gasolina", created_at=datetime.datetime.now())
                    nv.save()
                    print("Placa: " + placa + "Nuevo registro")

        if options['cargar_transporte_publico_gasoil']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0

            for file_line in file_list:
                nro_linea += 1
                try:
                    [placa] = file_line.split(",")
                    placa = placa.strip(' \t\n\r')
                    print(placa)
                except:
                   print('Error leyendo Linea nro: '+str(nro_linea))
                   print(file_line)
                   exit(0)

                try:
                    ta = Vehiculo.objects.get(placa=placa)
                    ta.tipo_vehiculo="TP Gasoil"
                    ta.save()
                except:
                    nv = Vehiculo(placa=placa, tipo_vehiculo="TP Gasoil", created_at=datetime.datetime.now())
                    nv.save()
                    print("Placa: " + placa + "Nuevo registro")

        if options['cargar_oficial_diario']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0
            tv = ''

            for file_line in file_list:
                nro_linea += 1
                try:
                    [placa, diario, inter_diario] = file_line.split(",")
                    inter_diario = inter_diario.strip(' \t\n\r')
                    print(placa)
                except:
                   print('Error leyendo Linea nro: '+str(nro_linea))
                   print(file_line)
                   exit(0)

                try:

                    if diario == 'X':
                        tv = "Oficial Diario"
                    elif inter_diario == "X":
                        tv = "Oficial Interdiario"

                    ta = Vehiculo.objects.get(placa=placa)
                    ta.tipo_vehiculo=tv
                    ta.save()
                except:
                    print("Placa: " + placa +"Ya no esta registrada")
                    mt_insert = Vehiculo(placa=placa, cedula='No regisrada', tipo_vehiculo=tv, cilindros=4)
                    mt_insert.save()

        if options['cola_verifica']:

            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0
            tv = ''


            # verifica carga
            for file_line in file_list:
                nro_linea += 1
                try:
                    [vehiculo, combustible, created_at] = file_line.split(",")
                    created_at = created_at.strip(' \t\n\r')
                    if len(vehiculo) > 7 or len(vehiculo) < 6:
                        print("Placa invalida", vehiculo)
                except Exception as e:
                   print('Error leyendo Linea nro: '+str(nro_linea))
                   print(e)
                   print(file_line)
                   exit(0)

        if options['cola_carga']:
            archivo = options['archivo']
            file_handle = open(archivo)
            file_list = file_handle.readlines()

            nro_linea = 0
            tv = ''
            fecha = ""

            for file_line in file_list:
                try:
                    [vehiculo, combustible, created_at] = file_line.split(",")
                    created_at = created_at.strip(' \t\n\r')
                    ta = Vehiculo.objects.get(placa=vehiculo)

                    try:
                        c = Cola(combustible_id=combustible,
                                 vehiculo_id=vehiculo,
                                 cargado=True,
                        )
                        c.save()
                    except:
                        print('Error insertando en cola: ' + vehiculo)

                except:
                    print("Placa: " + vehiculo + " Vehiculo no esta registrada")
                    mt_insert = Vehiculo(
                        placa=vehiculo,
                        cedula='No regisrada',
                        tipo_vehiculo="Particular",
                        cilindros=4)
                    mt_insert.save()

                    c = Cola(combustible_id=combustible,
                             vehiculo_id=vehiculo,
                             cargado=True,
                             )
                    c.save()
