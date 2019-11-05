from plotly import graph_objs as go
from plotly import offline
from plotly.subplots import make_subplots

from dgas.gas_app import models as md
from datetime import datetime, timedelta

import pandas as pd
from time import time

from django.db.models import F, Max, Min, Sum
from django.db import connections
from django.conf import settings

from dgas.supervisor_app.dash_app.get_data import load_data
from dgas.supervisor_app.dash_app.utils import format_date

def plot(figure):
    return offline.plot(
        figure, 
        output_type='div', 
        include_plotlyjs='cdn'
        )

def range_data(init, end, cmunicipio=None, cestacion=None):

    data = load_data(init=init, end=end)
    df_cola = data['df_cola']
    df_rebo = data['df_rebo']
    df_cont = data['df_cont']
    df_comb = data['df_comb']

    # Consultas

    stations = None
    if cestacion:
        stations = md.Estacion.objects.filter(id=cestacion.id)
    elif cmunicipio:
        stations = md.Estacion.objects.filter(municipio_estacion=cmunicipio)
    else:
        stations = md.Estacion.objects.all()

    df_stations = pd.read_sql(format_date(stations.values('id','nombre').query), 
        connections['default'], index_col='id')

    # Calculo de metricas por estaciones

    df_stations['atendidos'] = df_cola['id_estacion'].value_counts().reindex(df_stations.index, fill_value=0)
    df_stations['rebotados'] = df_rebo['id_estacion'].value_counts().reindex(df_stations.index, fill_value=0)

    df_stations['litros'] = df_cont.groupby(['id_estacion'])['cantidad'].max() - df_cont.groupby(['id_estacion'])['cantidad'].min()
    df_stations['litros'] = df_stations['litros'].fillna(0.0)

    df_stations['surtidos'] = df_comb.groupby(['estacion_id'])[
            ['litros_surtidos_g91','litros_surtidos_g95','litros_surtidos_gsl']
        ].sum().sum(axis=1).fillna(0).round(1)*1000

    df_stations['litros_per'] = (df_stations['litros']/df_stations['atendidos']).round(1)
    df_stations['surtido_per'] = (df_stations['surtidos']/df_stations['atendidos']).round(1)

    df_stations = df_stations[df_stations['atendidos']!=0]


    count_type = df_cola["type_car"][df_cola['id_estacion'].isin(df_stations.index)].value_counts()

    df_dates = pd.DataFrame(pd.date_range(init, end), columns=['day'])
    df_dates.index = df_dates['day']
    df_dates['count'] = df_cola['date'][df_cola['id_estacion'].isin(df_stations.index)].value_counts()[df_dates['day']]

    return {
            'stations': df_stations,
            'dates': df_dates, 
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
                    data['litros_per'],
                    data['surtido_per'],
                ]},
        )


def plotly_consult(init, end, municipio=None, parroquia=None, estacion=None):
    # Calculate data

    start = time()
    data = range_data(init, end, municipio)
    print("Time totals:", time()-start)

    stations = data['stations']
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
