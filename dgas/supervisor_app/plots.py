from plotly import graph_objs as go
from plotly import offline

from plotly.subplots import make_subplots

import pandas as pd
from dgas.gas_app import models as md
from datetime import datetime, timedelta
import re

plot = lambda figure: offline.plot(figure, output_type='div', include_plotlyjs='cdn')

def num_days_cola(init, end):
    print(init, end, init < end)
    start = init
    array = []
    days = []
    while start < end:
        array.append(md.Cola.objects.filter(created_at__range=(start, start + timedelta(days=1))).count())
        days.append(start.strftime('%d/%m'))
        start += timedelta(days=1)
    print(array, days)
    return (array, days)

def example_plotly():

    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Mining-BTC-180.csv")

    for i, row in enumerate(df["Date"]):
        p = re.compile(" 00:00:00")
        datetime = p.split(df["Date"][i])[0]
        df.iloc[i, 1] = datetime

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Mining-revenue-USD"],
            mode="lines",
            name="mining revenue"
        ),
        row=3, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Hash-rate"],
            mode="lines",
            name="hash-rate-TH/s"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
                        "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
                        "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
                font=dict(size=10),
                align="left"
            ),
            cells=dict(
                values=[df[k].tolist() for k in df.columns[1:]],
                align = "left")
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=800,
        showlegend=False,
        title_text="Bitcoin mining stats for 180 days",
    )

    return plot(fig)


def plotly_consult(init, end, municipio=None, parroquia=None, estacion=None):
    array, days = num_days_cola(init, end)
    fig = go.FigureWidget(go.Scatter(x=days, y=array, mode="lines"))
    return plot(fig)

