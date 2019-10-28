from .utils import format_date, input_to_date

import pandas as pd
from django.db.models import F, Max, Min, Sum
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db import connections

from dgas.gas_app import models as md
from dgas.users import models as us

def load_data(date_str):

    results = {}
    init = end = None

    # Validando fecha

    dates = input_to_date(date_str)

    if not dates:
        results['state'] = 'error'
    else:
        init, end = dates
        results['init'] = init
        results['end'] = end

    # Consultas en sql

    query_cola = md.Cola.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('combustible__estacion'),
                type_car=F('vehiculo__tipo_vehiculo'),
                id_municipio = F('combustible__estacion__municipio_estacion__id'),
                date=Cast('last_modified_at', DateField()),
            ).values(
                'id_municipio',
                'id_estacion',
                'vehiculo',
                'date',
                'cantidad',
                'type_car',
                
            ).query
    query_rebo = md.Rebotado.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('combustible__estacion'),
                type_car=F('vehiculo__tipo_vehiculo'),
                id_municipio = F('combustible__estacion__municipio_estacion'),
                date=Cast('last_modified_at', DateField()),
            ).values(
                'id_municipio',
                'id_estacion',
                'date',
                'type_car',
            ).query
    query_cont = md.ContadorMedida.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('contador__estacion'),
                id_municipio = F('contador__estacion__municipio_estacion'),
                date=Cast('last_modified_at', DateField()),
            ).values(
                'id_municipio',
                'id_estacion',
                'date',
                'cantidad',
            ).query
    query_comb  = md.Combustible.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_municipio = F('estacion__municipio_estacion')
            ).values(
                'id_municipio',
                'estacion',
                'litros_surtidos_g91',
                'litros_surtidos_g95',
                'litros_surtidos_gsl',
            ).query

    # Leyendo base de datos

    df_cola = pd.read_sql(format_date(query_cola), connections['default'])
    df_rebo = pd.read_sql(format_date(query_rebo), connections['default'])
    df_cont = pd.read_sql(format_date(query_cont), connections['default'])
    df_comb = pd.read_sql(format_date(query_comb), connections['default'])

    results['df_cola'] = df_cola
    results['df_rebo'] = df_rebo
    results['df_cont'] = df_cont
    results['df_comb'] = df_comb

    results['state'] = 'load'

    return results
