import re
from datetime import datetime, timedelta

import dash_html_components as html

def format_date(query):
    return re.sub(\
        r'[^\'\"]\d{4}\-\d{2}\-\d{2}[^\'\"]{0,1}',
        lambda m: " '"+m.group(0).replace(' ','')+"'::date ",
        str(query)\
    )


def input_to_date(date_str):
    if not date_str:
        return ()

    try:
        init, end = date_str.split('-')
        init = datetime.strptime(init, '%d/%m/%Y').date()
        end = datetime.strptime(end, '%d/%m/%Y').date()
        return (init, end)

    except ValueError:
        return ()

def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col.title()) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))] ,
        className = "table table-bordered table-hover",
    )

def box_bootstrap3(title="Box", content=[]):
    return html.Div([
            html.Div([html.H3(title, className="box-title")],
                className="box-header"),
            html.Div(content, className="box-body"),
            ],
        className="box box-primary")
