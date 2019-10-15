from plotly import graph_objs as go
from plotly import offline

from plotly.subplots import make_subplots

from dgas.gas_app import models as md
from datetime import datetime, timedelta

#from .example import *

from django.db.models import F, Max, Min, Sum

def plot(figure):
    return offline.plot(
        figure, 
        output_type='div', 
        include_plotlyjs='cdn'
        )

def plot_num_days_cola(init, end):
    start, array, days = init, [], []

    while start < end:
        array.append(md.Cola.objects.filter(created_at__range=(start, start + timedelta(days=1))).count())
        days.append(start.strftime('%d/%m'))
        start += timedelta(days=1)

    return go.Scatter(x=days, y=array, mode="lines", name='days_cola')


def range_data(init, end, cmunicipio=None, cestacion=None):
    # Total de litros, total de rebotados, promedio / vehiculo
    range_cola = md.Cola.objects\
            .filter(created_at__range=(init, end + timedelta(days=1,seconds=-1)))\
            .annotate(id_estacion=F('combustible__estacion'))
    range_rebo = md.Rebotado.objects\
            .filter(created_at__range=(init, end + timedelta(days=1,seconds=-1)))\
            .annotate(id_estacion=F('combustible__estacion'))
    range_cont = md.ContadorMedida.objects\
            .filter(created_at__range=(init, end + timedelta(days=1,seconds=-1)))\
            .annotate(id_estacion=F('contador__estacion'))
    range_comb  = md.Combustible.objects\
            .filter(created_at__range=(init, end + timedelta(days=1,seconds=-1)))

    num_rebotados = []
    num_vehiculos = []
    nombre_estacion = []
    litros_surtidos = []
    litros_consumidos = []

    def action_for_station(estacion):
        rebo_esta = range_rebo.filter(id_estacion=estacion.id)
        cola_esta = range_cola.filter(id_estacion=estacion.id)
        cont_esta = range_cont.filter(id_estacion=estacion.id)
        comb_esta = range_comb.filter(estacion=estacion)

        total_surtido = comb_esta.aggregate(
            total_litros= Sum('litros_surtidos_g91')+Sum('litros_surtidos_g95')+Sum('litros_surtidos_gsl')
            )['total_litros'] or 0
        total_consumido = cont_esta.aggregate(
            total_litros=Max('cantidad')-Min('cantidad')
            )['total_litros'] or 0
        total_rebotados = rebo_esta.count()
        total_cola = cola_esta.count()

        num_rebotados.append(total_rebotados)
        num_vehiculos.append(total_cola)
        litros_consumidos.append(total_consumido)
        litros_surtidos.append(total_surtido)

        nombre_estacion.append(estacion.nombre)


    if cestacion:
        action_for_station(cestacion)
    elif cmunicipio:
        for estacion in md.Estacion.objects.filter(municipio_estacion=cmunicipio):
            action_for_station(estacion)
    else:
        for estacion in md.Estacion.objects.all():
            action_for_station(estacion)

    return {
            'atendidos': num_vehiculos,
            'rebotados': num_rebotados, 
            'nombre_estacion': nombre_estacion,
            'consumo': litros_consumidos,
            'surtidos': litros_surtidos
            }


def result_table(data):
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
                    data['nombre_estacion'], 
                    data['atendidos'], 
                    data['rebotados'],
                    data['consumo'],
                    data['surtidos'],
                    [round(i/j,2) if j!= 0 else 0 for i,j in zip(data['consumo'], data['atendidos'])],
                    [round(i*1000/j,2) if j!=0 else 0 for i,j in zip(data['surtidos'], data['atendidos'])],
                ]},
        )


def plotly_consult(init, end, municipio=None, parroquia=None, estacion=None):
    # Calculate data
    data = range_data(init, end, municipio)

    # Initialize figure with subplots
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=False,
        specs=[[{"type": "table"}],
               [{"type": "table"}],
               [{"type": "bar"}],
               [{"type": "scatter"}],],
        subplot_titles=(
            "Resultados por Municipio", 
            "Resultados Generales", 
            "Número de Atendidos por Día", 
            "Número de Atendidos por Estación"),
        row_heights = [0.3, 0.1, 0.3, 0.3]
    )

    # Add traces

    fig.add_trace(
        plot_num_days_cola(init, end), 
        row=3, col=1)

    fig.add_trace(
        go.Bar(
            x=data['nombre_estacion'], 
            y=data['atendidos'],
            name="Atendidos",
            ), 
        row=4, col=1)

    fig.add_trace(
        go.Bar(
            x=data['nombre_estacion'], 
            y=data['rebotados'],
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
                        sum(data['atendidos']), 
                        sum(data['rebotados']),
                        sum(data['consumo']),
                        sum(data['surtidos'])*1000,
                    ]},
        ), 
        row=2, col=1)

    fig.add_trace(
        result_table(data), 
        row=1, col=1)

    # Update xaxis properties
    fig.update_xaxes(title_text="Días en el rango de fechas", row=3, col=1)
    fig.update_xaxes(title_text="Municipios", row=4, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Atendidos", row=3, col=1)
    fig.update_yaxes(title_text="Atendidos", row=4, col=1)

    # Update layout

    fig.update_layout(
        height=1200,
        showlegend=False,
        barmode='stack'
        )

    return plot(fig)

