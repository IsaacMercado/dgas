from .utils import query_to_dataframe, input_to_date

from django.db.models import F, Max, Min, Sum
from django.db.models.functions import Cast
from django.db.models.fields import DateField

from dgas.gas_app import models as md
from dgas.users import models as us

def load_data(date_str=None, init=None, end=None):

    results = {'state':'error'}

    # Validando fecha

    if date_str:
        dates = input_to_date(date_str)
        if dates:
            init, end = dates
        else:
            return results
    else:
        if not (init and end):
            return results

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
                date=Cast('created_at', DateField()),
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
                date=Cast('created_at', DateField()),
            ).values(
                'id_municipio',
                'id_estacion',
                'date',
                'cantidad',
            ).query
    query_comb  = md.Combustible.objects\
            .filter(fecha_planificacion__range=(init, end))\
            .annotate(
                id_municipio = F('estacion__municipio_estacion')
            ).values(
                'id_municipio',
                'estacion',
                'litros_surtidos_g91',
                'litros_surtidos_g95',
                'litros_surtidos_gsl',
            ).query

    results['df_cola'] = query_to_dataframe(query_cola)
    results['df_rebo'] = query_to_dataframe(query_rebo)
    results['df_cont'] = query_to_dataframe(query_cont)
    results['df_comb'] = query_to_dataframe(query_comb)

    results['state'] = 'load'

    return results
