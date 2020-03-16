from flask import Flask, render_template
import pandas as pd
import plotly
import json
import plotly.graph_objs as go
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from waitress import serve

# import logging
# from console_log import ConsoleLog

# logger = logging.getLogger('console')
# logger.setLevel(logging.DEBUG)

tesla = pd.read_csv("data/tesla.csv")
tesla["Date"] = pd.to_datetime(tesla["Date"])

tesla["Year"] = [date.year for date in tesla["Date"]]
tesla["Month"] = [date.month for date in tesla["Date"]]
tesla["Day"] = [date.day for date in tesla["Date"]]

monthly = tesla.groupby(["Year", "Month"])
yearly = tesla.groupby(["Year"])

monthly_means = pd.DataFrame({
    "Open"      : monthly["Open"].mean(),
    "High"      : monthly["High"].mean(),
    "Low"       : monthly["Low"].mean(),
    "Close"     : monthly["Close"].mean(),
    "Volume"    : monthly["Volume"].mean(),
    "Adj Close" : monthly["Adj Close"].mean(),
}).reset_index()

monthly_means['Date'] = pd.to_datetime({
    "year"  : monthly_means["Year"],
    "month" : monthly_means["Month"],
    "day"   : [15]*len(monthly_means["Month"]),
})

monthly_means = monthly_means.drop(["Year", "Month"], axis=1)

yearly_means = pd.DataFrame({
    "Open"      : yearly["Open"].mean(),
    "High"      : yearly["High"].mean(),
    "Low"       : yearly["Low"].mean(),
    "Close"     : yearly["Close"].mean(),
    "Volume"    : yearly["Volume"].mean(),
    "Adj Close" : yearly["Adj Close"].mean(),
}).reset_index()

yearly_means['Date'] = pd.to_datetime({
    "year"  : yearly_means["Year"],
    "month" : [6]*len(yearly_means["Year"]),
    "day"   : [1]*len(yearly_means["Year"]),
})
yearly_means = yearly_means.drop(["Year"], axis=1)


import plotly.graph_objects as go

fig_high_low = go.Figure()
fig_high_low.add_trace(
    go.Scatter(
        x = monthly_means["Date"],
        y = monthly_means["High"],
        name = "High"
    ))
fig_high_low.add_trace(
    go.Scatter(
        x=monthly_means["Date"],
        y=monthly_means["Low"],
        name = "Low"
    ))
fig_high_low.update_layout(
    go.Layout(
        margin={"l":40}
    ))

fig_open_close = go.Figure()
fig_open_close.add_trace(
    go.Scatter(
        x = monthly_means["Date"],
        y = monthly_means["Open"],
        name = "Open"
    ))
fig_open_close.add_trace(
    go.Scatter(
        x=monthly_means["Date"],
        y=monthly_means["Close"],
        name = "Close"
    ))
fig_open_close.update_layout(
    go.Layout(
        margin={"l":40}
    ))


app = dash.Dash()

colors = {
    "background": "white",
    "text": "#7FDBFF"
}

title = {
    "font-family":"Arial, Helvetica, sans-serif",
    "display": "inline-block",
    "color": "white",
    "text-align": "center",
    "padding": "4px 10px",
    "text-decoration": "none",
    "background": "grey",
}

navbar = {
    "font-family":"Arial, Helvetica, sans-serif",
    "display": "inline-block",
    "color": "white",
    "text-align": "center",
    "padding": "4px 10px",
    "text-decoration": "none",
    "background": "grey",
}

app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[
    html.Div(
        children=[
            html.H2(
                "Tesla Stock Price",
                style=title
            ), 
            dcc.Dropdown(
                options=[
                    {'label': 'Monthly mean high and low values', 'value': 'mhl'},
                    {'label': 'Monthly mean opening and closing values', 'value': 'moc'},
                ],
                placeholder="Select graph to be shown",
                multi=True,
                id="dropdown"
            )  
        ],
        style={"background":"grey"}
    ),
    html.Div([], id='output')
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


@app.callback(Output('output', 'children'), [Input('dropdown', 'value')])

def show_hide_element(selected_values):
    graphs = []

    if selected_values is None:
        selected_values = []

    if 'mhl' in selected_values:
        graphs.append(
            html.Div([
            html.H4("Monthly mean high and low values"),
            dcc.Graph(
                id="monthly_high_low",
                figure=fig_high_low,

            ),], style={"text-align":"center", "margin-top":10}),
        )
    if 'moc' in selected_values:
        graphs.append(
            html.Div([
            html.H4("Monthly mean opening and closing values"),
            dcc.Graph(
                id="monthly_open_close",
                figure=fig_open_close,
            ),], style={"text-align":"center", "margin-top":10}),
        )
    return graphs

class Dashboard:

    @staticmethod
    def run():
        import os
        try:
            PORT = os.getenv["PORT"]
        except:
            PORT = 8000
        serve(app.server, host="0.0.0.0", port=PORT)
    
    @staticmethod
    def test():
        print("Hello world!")
