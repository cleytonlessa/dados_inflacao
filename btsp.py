#importando as bibliotecas
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash import callback
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

#escolhendo o tema
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

#criando um grid
grid = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown({'^BVSP': 'IBOV', 'PETR4.SA': 'PETR4', 'VALE3.SA': 'VALE3'}, '^BVSP', id='lista-tickers'), md=4),
                dbc.Col(dcc.Dropdown({'plotly_white': 'Branco', 'ggplot2': 'Cinza', 'plotly_dark': 'Preto'}, 'plotly_white', id='lista-templates'),md=4),
                dbc.Col(dcc.Dropdown({'a': 'Colorido', 'b': 'Preto e Branco'}, 'a', id='lista-cores'), md=4),
            ]
        ),
        dbc.Row(
            [
                #dbc.Col(dcc.Graph(), md=4),
                dbc.Col(dcc.Graph(id='graph',),md=12)
            ]
        )
    ]
)

#inserindo a navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

#montagem do layout
app.layout = html.Div(
    [   
        #inserindo a navbar
        navbar,
        dbc.Container(
            [   
                grid
            ]
        )
    ]
)

@callback(
    Output('graph', 'figure'),
    Input('lista-tickers', 'value'),
    Input('lista-templates', 'value'),
    Input('lista-cores', 'value'),
)
def update_output(ticker, template, pb):
    # Obter a data atual
    today = datetime.today()

    # Retroceder para a última sexta-feira passada
    last_friday = today - timedelta(days=today.weekday() + 3, weeks=0)

    # Retroceder mais 4 dias para obter a data de início (últimos 5 dias úteis)
    start_date = last_friday - timedelta(days=4)

    #ticker = value#"^BVSP"#"BOVA11.SA"#"^BVSP"
    # Obter os dados do índice IBOV para as datas especificadas
    df = yf.download(f'{ticker}', start='1953-01-01', end=today)
    df = df.rename_axis('data').reset_index()

    #template='ggplot2'
    fig = go.Figure(
            data=[go.Candlestick(
              x=df['data'],
              open=df['Open'],
              high=df['High'],
              low=df['Low'],
              close=df['Close'],
            )],
            layout=go.Layout(
              title=go.layout.Title(text=f'{ticker}'),
              template=template,
            )
        )

    if(pb == 'b'):
        cs = fig.data[0]

        # Set line and fill colors
        cs.increasing.fillcolor = '#FFF'
        cs.increasing.line.color = '#FFF'
        cs.decreasing.fillcolor = '#000'
        cs.decreasing.line.color = '#000'
    
    return fig

if __name__ == "__main__":
    #app.run_server(debug=True, port=8888)
    app.run_server(debug=True)