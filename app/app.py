# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import os
import json
import flask
import base64

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

import plotly.graph_objs as go

app = dash.Dash(__name__)
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#FFFFFF',    # white
    'text': '#111111'           # black
}

styles = {
    'column': {
        'display': 'inline-block',
        'width': '33%',
        'padding': 10,
        'boxSizing': 'border-box',
        'minHeight': '200px'
    },
    'pre': {'border': 'thin lightgrey solid'}
}

# import data for use
exec(open("load_data.py").read())

# create base map for country selection
exec(open("map/map.py").read())

image_filename = 'test.jpg' # replace with your own image
encoded_image = base64.b64encode(open('test.jpg', 'rb').read())

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, 
    children=[
        html.H1(
            children='Welcome to Global Village!',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.H3(
            children='See stories about kids in other United Nations Countries',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div('What is your name?',
            style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),

        dcc.Input(type='text',
            style={
            'textAlign': 'center',
            'color': colors['text']
            }),

        html.Div('Are you a boy or a girl?',
            style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),

        dcc.RadioItems(
            options=[
                {'label': 'Boy', 'value': 'girl'},
                {'label': 'Girl', 'value': 'boy'},
            ],
            value='MTL'
        ),

        html.Div('Select your topics:', 
            style={
            'textAlign': 'center',
            'color': colors['text']
            }
        ),

        dcc.Dropdown(
            id = 'select-topic',
            options=[{'label': s, 'value': s} for s in topics],
            multi=True,
        ),

        dcc.Graph(
            id = 'world-map',
            figure = world_map_fig
        ),
        
        # html.H3(id = 'topic-picture'),

        html.Div([
            dcc.Markdown("""
                Your country is:
                """.replace('    ', '')),
                html.H3(id = 'click-country'),

            dcc.Markdown("""
                Your topics are:
                """.replace('    ', '')),
        
            html.Div('Here is an image from the country you selected:', 
                style={
                'textAlign': 'center',
                'color': colors['text']
                }
            ),

            html.Img(src='data:image/jpeg;base64,{}'
                        .format(encoded_image.decode("utf-8"))),

            html.H3(id = 'topic-selection'),

            html.H5(id = "country-text")

        ]),

    ])

@app.callback(
    Output('click-country', 'children'),
    [Input('world-map', 'clickData')])
def update_country_click(clickData):
    if clickData is not None:
        return clickData['points'].pop(0)['text']

@app.callback(
    dash.dependencies.Output('country-text', 'children'),
    [dash.dependencies.Input('world-map', 'clickData')])
def update_country_text(dropdown_value):
    if dropdown_value is not None:
        value_text = dropdown_value['points'].pop(0)['text']
        country_text = (simple_wiki[simple_wiki.name == value_text]
                            .clean_summary
                            .values[0])
    else:
        country_text = ""

    return " ".join(sent_tokenize(country_text)[:5])

@app.callback(
    Output('topic-selection', 'children'),
    [Input('select-topic', 'value')])
def update_topic(selection):
    if selection is not None:
        return ', '.join(selection)
    else: 
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)