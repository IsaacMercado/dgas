# coding=utf-8
import string
import traceback

from django.core.management.base import BaseCommand
from dgas.gas_app.models import Vehiculo


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


