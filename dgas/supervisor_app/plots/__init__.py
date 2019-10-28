from plotly import graph_objs as go
from plotly import offline
from plotly.subplots import make_subplots

from dgas.gas_app import models as md
from datetime import datetime, timedelta

import pandas as pd
from time import time

from django.db.models import F, Max, Min, Sum
from django.conf import settings

def plot(figure):
    return offline.plot(
        figure, 
        output_type='div', 
        include_plotlyjs='cdn'
        )

def range_data(init, end, cmunicipio=None, cestacion=None):

    # Consultas

    range_cola = md.Cola.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('combustible__estacion'),
                type_car=F('vehiculo__tipo_vehiculo'),
                id_municipio = F('combustible__estacion__municipio_estacion')
            )
    range_rebo = md.Rebotado.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('combustible__estacion'),
                type_car=F('vehiculo__tipo_vehiculo'),
                id_municipio = F('combustible__estacion__municipio_estacion')
            )
    range_cont = md.ContadorMedida.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_estacion=F('contador__estacion'),
                id_municipio = F('contador__estacion__municipio_estacion')
            )
    range_comb  = md.Combustible.objects\
            .filter(created_at__date__range=(init, end))\
            .annotate(
                id_municipio = F('estacion__municipio_estacion')
            )

    stations = None
    if cestacion:
        stations = md.Estacion.objects.filter(id=cestacion.id)
    elif cmunicipio:
        stations = md.Estacion.objects.filter(municipio_estacion=cmunicipio)
    else:
        stations = md.Estacion.objects.all()

    # Convertir a DataFrame

    df_cola = pd.DataFrame(range_cola.values(
        'cantidad',
        'created_at',
        'last_modified_at',
        'id_estacion',
        'type_car',
        'id_municipio'
        ))
    df_cola['created_at'] = df_cola['created_at'].dt.date
    df_cola['last_modified_at'] = df_cola['last_modified_at'].dt.date

    df_rebo = pd.DataFrame(range_rebo.values(
        'created_at',
        'last_modified_at',
        'id_estacion',
        'type_car',
        'id_municipio'
        ))
    df_rebo['created_at'] = df_rebo['created_at'].dt.date
    df_rebo['last_modified_at'] = df_rebo['last_modified_at'].dt.date

    if range_cont:
        df_cont = pd.DataFrame(range_cont.values(
            'cantidad',
            'created_at',
            'id_estacion',
            'id_municipio'
            ))
        df_cont['created_at'] = df_cont['created_at'].dt.date
    else:
        df_cont = None

    if range_comb:
        df_comb = pd.DataFrame(range_comb.values(
            'id_municipio',
            'litros_surtidos_g91',
            'litros_surtidos_g95',
            'litros_surtidos_gsl',
            'estacion',
            ))
    else:
        df_comb = None

    df_stations = pd.DataFrame(stations.values('id', 'nombre'))
    df_stations.index = df_stations['id']

    # Variables

    df_dates = count_type  = df_smooth = None

    # Calculo de metricas

    df_stations['atendidos'] = df_stations['id'].apply(
        lambda x: df_cola['id_estacion'][df_cola['id_estacion']==x].count()
    )
    df_stations['rebotados'] = df_stations['id'].apply(
        lambda x: df_rebo['id_estacion'][df_rebo['id_estacion']==x].count()
    )

    if df_cont:
        def size_range(x):
            col = df_cont['cantidad'][df_cont['id_estacion']==x]
            return col.max()-col.min()

        df_stations['litros'] = df_stations['id'].apply(
            #lambda x: df_cont[df_cont['id_estacion']==x].sort_values('created_at')['cantidad'].diff().sum()
            size_range
        )
    else:
        df_stations['litros'] = 0.0


    if range_comb:
        df_stations['surtidos'] = df_stations['id'].apply(
            lambda x: df_comb[df_comb['estacion']==x][
                    ['litros_surtidos_g91','litros_surtidos_g95','litros_surtidos_gsl']
                ].sum().sum()
        )
    else:
        df_stations['surtidos'] = 0.0

    count_type = pd.value_counts(df_cola["type_car"][df_cola['id_estacion'].isin(df_stations['id'])])

    df_dates = pd.DataFrame(pd.date_range(init, end), columns=['day'])
    df_dates.index = df_dates['day']
    df_dates['count'] = df_dates['day'].apply(
            lambda x: df_cola['created_at'][(df_cola['created_at']==x) & (df_cola['id_estacion'].isin(df_stations['id']))].count()
        )

    return {
            'stations': df_stations,
            'dates': df_dates, 
            'smooth': df_smooth,
            'types': count_type
            }


def result_table(dict_data):
    data = dict_data['stations']
    return go.Table(
        header = {'values': [
                    "Estacion", 
                    "Atendidos", 
                    "Rebotados",
                    "Lts. Consumidos",
                    "Lts. Surtidos",
                    "Consumo/Vehiculo",
                    "Surtido/Vehiculo"
                ]},
        cells = {'values': [
                    data['nombre'], 
                    data['atendidos'], 
                    data['rebotados'],
                    data['litros'],
                    data['surtidos'],
                    (data['litros']/data['atendidos']).round(1),
                    (data['surtidos']*1000/data['atendidos']).round(1),
                ]},
        )


def plotly_consult(init, end, municipio=None, parroquia=None, estacion=None):
    # Calculate data

    start = time()
    data = range_data(init, end, municipio)
    print("Time totals:", time()-start)

    stations = data['stations']
    smooth = data['smooth']
    type_car = data['types']
    dates_time = data['dates']

    # Initialize figure with subplots
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=False,
        specs=[[{"type": "table"}],
               [{"type": "table"}],
               [{"type": "bar"} if init == end else {"type": "scatter"}],
               [{"type": "bar"}],],
        subplot_titles=(
            "Resultados por Municipio", 
            "Resultados Generales", 
            "Número de Vehículos Atendidos por Tipo" if init == end else "Número de Atendidos por Día", 
            "Número de Atendidos por Estación"),
        row_heights = [0.3, 0.1, 0.3, 0.3]
    )

    # Add traces

    if init == end:
        fig.add_trace(
            go.Bar(
                x=type_car.index, 
                y=type_car, 
                name='Atendidos',
                text=type_car,
                textposition='auto',
                ), 
            row=3, col=1)
    else:
        fig.add_trace(
            go.Scatter(
                x=dates_time['day'],
                y=dates_time['count'], 
                mode="lines", name='Atendidos'), 
            row=3, col=1)

    fig.add_trace(
        go.Bar(
            x=stations['nombre'], 
            y=stations['atendidos'],
            name="Atendidos",
            ), 
        row=4, col=1)

    fig.add_trace(
        go.Bar(
            x=stations['nombre'], 
            y=stations['rebotados'],
            name="Rebotados",
            ), 
        row=4, col=1)

    fig.add_trace(
        go.Table(
            header = {'values': [
                        "Atendidos", 
                        "Rebotados",
                        "Lts. Consumidos",
                        "Lts. Surtidos",
                    ]},
            cells = {'values': [
                        stations['atendidos'].sum(), 
                        stations['rebotados'].sum(),
                        stations['litros'].sum(),
                        stations['surtidos'].sum()*1000,
                    ]},
        ), 
        row=2, col=1)

    fig.add_trace(
        result_table(data), 
        row=1, col=1)


    if not init == end:
        fig.update_xaxes(title_text="Días en el rango de fechas", row=3, col=1)
    else:
        fig.update_xaxes(title_text="Tipo de Vehículos", row=3, col=1)
    fig.update_yaxes(title_text="Atendidos", row=3, col=1)

    fig.update_xaxes(title_text="Estaciones", row=4, col=1)
    fig.update_yaxes(title_text="Atendidos", row=4, col=1)

    fig.update_layout(
        height=1200,
        showlegend=False,
        barmode='stack'
        )

    return plot(fig)
