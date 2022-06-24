from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import http.client

conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "1ccbf53bf9msh87da6152e36bfb4p18ba64jsnda22b3792ae5",
    'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
    }

conn.request("GET", "/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=compact&datatype=json", headers=headers)

res = conn.getresponse()





app = Dash(__name__)

app.layout = html.Div([
    html.H4('Apple stock candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    dat = res.read()
    data=dat.decode('utf-8')# replace with your own data source
    fig = go.Figure(go.Candlestick(
        x=data.index,
        open=data[format(open)],
        high=data['high'],
        low=data['low'],
        close=data['close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)