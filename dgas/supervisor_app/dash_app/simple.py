import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from django_plotly_dash import DjangoDash
from django.db import connections
from django.db.models import F, Max, Min, Sum, Q, Count
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core.cache import cache

from datetime import datetime, timedelta
from time import time
import pandas as pd
from plotly import graph_objs as go

from dgas.gas_app import models as md
from dgas.users import models as us

from .utils import format_date, input_to_date, generate_table, box_bootstrap3
from .get_data import load_data

NOT_DATA = "No se han cargado datos."
MINUTOS = 5

app = DjangoDash('SupervisorApp')   # replaces dash.Dash

app.layout = html.Div([

    box_bootstrap3("Consulta", [
        html.Label('Rango de fechas'),
        html.Br(),
        dcc.Input(
            id='input-range-date', 
            type='text', 
            className='form-control pull-right',
        ),
        html.Br(),
        dcc.Loading(id="loading-01", children=[html.Div(id='message-date'),], type="dot"),
        html.Br(),

        html.Label('Municipios'),
        dcc.Dropdown(
            id='municipios',
            placeholder='Municipios',
            options=[{"label": mun.municipio, "value": mun.id} for mun in us.Municipio.objects.all()],
            multi=True
        ),
        
        html.Label('Parroquias'),
        dcc.Dropdown(
            id='parroquias',
            multi=True,
            placeholder='Parroquias',
            disabled=True
        ),

        html.Label('Estaciones'),
        dcc.Dropdown(
            id='estaciones',
            placeholder='Estaciones',
            multi=True
        ),
        html.Br(),

        html.Button(
            'Consultar',
            id='submit-button',
            className='btn btn-primary',
        ),
        html.Br(),

        dcc.Interval(id='interval-time', interval=5*1000, n_intervals=0),
        html.Div(id='message-time-computo'),
        html.Br(),
        ]),
    
    box_bootstrap3( "Resultados", [

        html.Center([html.H4('Resultados por Estación'),]),

        dcc.Loading(id="loading-1", children=[

            dash_table.DataTable(
                id='table-estaciones',
                columns=[
                        {"name": 'Estación', "id": 'nombre'},
                        {"name": 'Atendidos', "id": 'atendidos'},
                        {"name": 'Rebotados', "id": 'rebotados'},
                        {"name": 'Consumido', "id": 'litros'},
                        {"name": 'Surtidos', "id": 'surtidos'},
                        {"name": 'Consumo/Vehiculo', "id": 'litros_per'},
                        {"name": 'Surtido/Vehiculo', "id": 'surtido_per'},
                    ],
                style_cell={
                    'textAlign': 'left',
                    'font-family':'sans-serif',
                    'maxHeight': '70px',
                    'border': 'thin lightgrey solid'
                },
                export_format='csv',
                export_headers='display',
                merge_duplicate_headers=True,
                include_headers_on_copy_paste=True,
                fixed_rows={ 'headers': True, 'data': 0 },
                sort_action='native',
                ),

            ], type="default"),


    
        html.Br(),

        html.Center([html.H4('Resultados Generales'),]),


        dcc.Loading(id="loading-2", children=[
            dash_table.DataTable(
                id='table-general',
                columns=[
                        {"name": 'Atendidos', "id": 'atendidos'},
                        {"name": 'Rebotados', "id": 'rebotados'},
                        {"name": 'Consumido', "id": 'litros'},
                        {"name": 'Surtidos', "id": 'surtidos'},
                        {"name": 'Consumo/Vehiculo', "id": 'litros_per'},
                        {"name": 'Surtido/Vehiculo', "id": 'surtido_per'},
                    ],
                style_cell={
                    'textAlign': 'left',
                    'font-family':'sans-serif',
                    'border': 'thin lightgrey solid'
                    },
                ),
            ], type="default"),

        html.Br(),

        html.Center([html.H4('Vehiculos con mayor número de cargas'),]),

        dcc.Loading(id="loading-3", children=[
            dash_table.DataTable(
                id='table-vehiculo-cargas',
                columns=[
                        {"name": 'Placa', "id": 'placa'},
                        {"name": 'Número de carga', "id": 'vehiculo_id'},
                        ],
                style_cell={
                    'textAlign': 'left',
                    'font-family':'sans-serif',
                    },
                page_current=0,
                page_size=10,        
                page_action='custom',
                export_format='csv',
                export_headers='display',
                merge_duplicate_headers=True,
                include_headers_on_copy_paste=True,
                ),
            ], type="default"),

        html.Br(),
        html.Br(),

        dcc.Loading(id="loading-4", children=[html.Div(id='graph-div-01'),]),
        dcc.Checklist(
            id='is-smooth',
            options=[{'label': 'Suavizar datos', 'value': 'smooth'},],
        ),
        html.Br(),

        dcc.Loading(id="loading-5", children=[html.Div(id='graph-div-02'),]),
        html.Br(),

        dcc.Loading(id="loading-6", children=[html.Div(id='graph-div-03'),]),
        html.Br(),

        ]),

    box_bootstrap3( "Generales", [
        dcc.Loading(id="loading-7", children=[html.Div(id='graph-div-04')]),
        ]),

    ])

@app.callback(
    Output('message-time-computo', 'children'),
    [Input('interval-time', 'n_intervals')])
def callback_update_interval(n):
    if 'dataframes' in cache:
        data = cache.get('dataframes')
        init, end = data['init'], data['end']
        if 'df_stations' in cache:
            pass
        return "Datos cargados. Del " + init.strftime("%d/%m/%Y") + " al " + end.strftime("%d/%m/%Y")
    return "Datos sin cargar. Por favor seleccione una fecha."

@app.callback(
    Output('estaciones', 'options'), 
    [Input('municipios', 'value')]
    )
def callback_select_municipio(municipios_ids):
    print(cache.get('my_new_key'), municipios_ids)
    if  municipios_ids:
        return [{"label": es.nombre, "value": es.id} for es in md.Estacion.objects.filter(municipio_estacion__id__in=municipios_ids)]
    return []

@app.callback(
    Output('message-date', 'children'), 
    [Input('input-range-date', 'value')])
def callback_read_date(date_str):
    if not date_str:
        return "Por favor selecione una fecha para cargar los datos."
    start = time()
    data = load_data(date_str)
    init, end = data['init'], data['end']
    cache.set("dataframes", data, 60*MINUTOS)
    return 'Datos cargados. Tiempo de carga: ' + str(round(time()-start, 2)) + ' segundos.'

@app.callback(
    Output('table-estaciones', 'data'), 
    [Input('submit-button', 'n_clicks')],
    [
        State('input-range-date', 'value'),
        State('municipios', 'value'),
        State('parroquias', 'value'),
        State('estaciones', 'value'),
    ])
def callback_query(n_clicks, date, municipios, parroquias, estaciones):

    white = [{
        'atendidos': '',
        'rebotados': '',
        'litros': '',
        'surtidos': '',
        'litros_per': '',
        'surtido_per': '',
        }]

    # Iniciando varibles

    df_stations = df_dates = count_type  = df_smooth = None
    df_cola = df_rebo = df_cont = df_comb = init = end = None

    # Validando fecha

    dates = input_to_date(date)

    if not dates:
        return white
    else:
        init, end = dates

    dfs = cache.get_or_set('dataframes', load_data(date), 60*MINUTOS)

    if dfs['state'] == 'load':

        if not (dfs['init'], dfs['end']) == (init, end):
            cache.set('dataframes', load_data(date), 60*MINUTOS)
            dfs = cache.get('dataframes')
            if dfs and (dfs['state'] == 'load'):
                df_cola = dfs['df_cola']
                df_rebo = dfs['df_rebo']
                df_cont = dfs['df_cont']
                df_comb = dfs['df_comb']

                init = dfs['init']
                end = dfs['end']
            else:
                return white
        else:
            df_cola = dfs['df_cola']
            df_rebo = dfs['df_rebo']
            df_cont = dfs['df_cont']
            df_comb = dfs['df_comb']

            init = dfs['init']
            end = dfs['end']
    else:
        return white

    # Filtrando por estaciones

    if estaciones:
        stations = md.Estacion.objects.filter(id__in=estaciones)
    elif parroquias:
        pass
    elif municipios:
        stations = md.Estacion.objects.filter(municipio_estacion__id__in=municipios)
    else:
        stations = md.Estacion.objects.all()

    df_stations = pd.read_sql(format_date(stations.values('id','nombre').query), 
        connections['default'], index_col='id')

    df_stations['atendidos'] = df_cola['id_estacion'].value_counts().reindex(df_stations.index, fill_value=0)
    df_stations['rebotados'] = df_rebo['id_estacion'].value_counts().reindex(df_stations.index, fill_value=0)

    df_stations['litros'] = df_cont.groupby(['id_estacion'])['cantidad'].max() - df_cont.groupby(['id_estacion'])['cantidad'].min()
    df_stations['litros'] = df_stations['litros'].fillna(0.0)

    df_stations['surtidos'] = df_comb.groupby(['estacion_id'])[
            ['litros_surtidos_g91','litros_surtidos_g95','litros_surtidos_gsl']
        ].sum().sum(axis=1).fillna(0).round(1)

    df_stations['litros_per'] = (df_stations['litros']/df_stations['atendidos']).round(1)
    df_stations['surtido_per'] = (df_stations['surtidos']/df_stations['atendidos']).round(1)

    df_stations = df_stations[df_stations['atendidos']!=0]

    cache.set('df_stations', df_stations, 60*MINUTOS)

    return df_stations[
            ['nombre','atendidos','rebotados','litros','surtidos','litros_per','surtido_per']
        ].to_dict('records')

@app.callback(
    Output('table-general', 'data'), 
    [Input('table-estaciones', 'data')])
def callback_general_result(event):
    df_stations = cache.get('df_stations')
    if df_stations is None:
        return [{
            'atendidos': '',
            'rebotados': '',
            'litros': '',
            'surtidos': '',
            'litros_per': '',
            'surtido_per': '',
            }]
    return [{
                'atendidos': df_stations['atendidos'].sum(),
                'rebotados': df_stations['rebotados'].sum(),
                'litros': df_stations['litros'].sum(),
                'surtidos': df_stations['surtidos'].sum(),
                'litros_per': df_stations['litros_per'].mean(),
                'surtido_per': df_stations['surtido_per'].mean(),
            }]

@app.callback(
    Output('table-vehiculo-cargas', 'data'),
    [Input('table-vehiculo-cargas', "page_current"),
     Input('table-vehiculo-cargas', "page_size"),
     Input('table-estaciones', 'data')])
def update_table(page_current, page_size, data):

    df_stations = cache.get('df_stations')
    dfs = cache.get('dataframes')

    if (not df_stations is None) and (not df_stations is None) and (dfs['state'] == 'load'):
        df_cola = dfs['df_cola']
    else:
        return [{'placa':'','vehiculo_id':''}]

    count_placas = df_cola["vehiculo_id"][df_cola['id_estacion'].isin(df_stations.index)].value_counts()[:100]
    df_placas = pd.DataFrame(count_placas)
    df_placas['placa'] = count_placas.index
    return df_placas.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records')

@app.callback(
    Output('graph-div-01', 'children'), 
    [
        Input('table-estaciones', 'data'),
        Input('is-smooth', 'value'),
    ])
def callback_time_result(event, is_smooth):
    # Linea de tiempo
    dfs = cache.get('dataframes')
    df_stations = cache.get('df_stations')
    if (not dfs is None) and (dfs['state'] == 'load') and (not df_stations is None):
        df_cola = dfs['df_cola']
        init = dfs['init']
        end = dfs['end']
    else:
        return NOT_DATA

    if init != end:
        df_dates = pd.DataFrame(pd.date_range(init, end), columns=['day'])
        df_dates.index = df_dates['day']
        df_dates['count'] = df_cola['date'][df_cola['id_estacion'].isin(df_stations.index)].value_counts()[df_dates['day']]

        trazes = []

        trazes.append(
            go.Scatter(
                x=df_dates['day'],
                y=df_dates['count'], 
                mode="lines", name='Atendidos')
            )

        if is_smooth and ('smooth' in is_smooth):
            from statsmodels.nonparametric.smoothers_lowess import lowess
            result = lowess(df_dates['count'], df_dates['day'])
            df_smooth = pd.DataFrame(result, columns=['day','count'])
            df_smooth['day'] = pd.to_datetime(df_smooth['day'])

            trazes.append(
                go.Scatter(
                    x=df_smooth['day'],
                    y=df_smooth['count'], 
                    mode="lines", name='Atendidos')
                )

        return dcc.Graph(
                id='graph-01',
                figure={
                    'data': trazes,
                    'layout': go.Layout(
                        autosize=True,
                        title={"text": 'Número de Atendidos por Día'},
                        xaxis={'title': 'Días en el rango de fechas'},
                        yaxis={'title': 'Atendidos'}
                    )
                }
            )
    else:
        return "En un solo día no se puede gráficar la linea de tiempo"

@app.callback(
    Output('graph-div-02', 'children'), 
    [Input('table-estaciones', 'data')])
def callback_type_result(event):

    df_stations = cache.get('df_stations')
    dfs = cache.get('dataframes')
    if (not df_stations is None) and (not df_stations is None) and (dfs['state'] == 'load'):
        df_cola = cache.get('dataframes')['df_cola']
        df_stations = cache.get('df_stations')
        dfs = cache.get('dataframes')
    else:
        return NOT_DATA

    # Tipos de vehiculo

    count_type = df_cola["type_car"][df_cola['id_estacion'].isin(df_stations.index)].value_counts()

    return dcc.Graph(
            id='graph-02',
            figure={
                'data': [
                    go.Bar(
                        x=count_type.index, 
                        y=count_type, 
                        name='Atendidos',
                        text=count_type,
                        textposition='auto',
                        )
                ],
                'layout': go.Layout(
                    autosize=True,
                    title={"text": 'Número de Vehículos Atendidos por Tipo'},
                    xaxis={'title': 'Tipo de Vehículos'},
                    yaxis={'title': 'Atendidos'}
                )
            }
        )

@app.callback(
    Output('graph-div-03', 'children'), 
    [Input('table-estaciones', 'data')])
def callback_cola_plot_result(event):
    
    if not 'df_stations' in cache:
        return NOT_DATA

    df_stations = cache.get('df_stations')

    # Distribucion por estaciones

    return dcc.Graph(
            id='graph-03',
            figure={
                'data': [
                    go.Bar(
                        x=df_stations['nombre'], 
                        y=df_stations['atendidos'],
                        name="Atendidos",
                        ),
                    go.Bar(
                        x=df_stations['nombre'], 
                        y=df_stations['rebotados'],
                        name="Rebotados",
                        ),
                ],
                'layout': go.Layout(
                    barmode = 'stack',
                    autosize=True,
                    title={"text": 'Número de Atendidos por Estación'},
                    xaxis={'title': 'Estaciones'},
                    yaxis={'title': 'Atendidos'}
                )
            })

@app.callback(
    Output('graph-div-04', 'children'), 
    [Input('submit-button', 'n_clicks')])
def callback_municipio_plot_result(event):

    values = md.Vehiculo.objects.exclude(Q(usuario__isnull=True)|Q(usuario__municipio__isnull=True)).\
        values('usuario__municipio').\
        order_by('usuario__municipio').\
        annotate(nombre=F('usuario__municipio__municipio'), count=Count('usuario__municipio')).\
        order_by('nombre')

    # Distribucion por estaciones

    return dcc.Graph(
            id='graph-04',
            figure={
                'data': [
                    go.Bar(
                        x=[mun['nombre'] for mun in values], 
                        y=[mun['count'] for mun in values],
                        ),
                ],
                'layout': go.Layout(
                    barmode = 'stack',
                    autosize=True,
                    title={"text": 'Número de Vehículos por Municipio'},
                    xaxis={'title': 'Municipios'},
                    yaxis={'title': 'Vehículos'}
                )
            })
