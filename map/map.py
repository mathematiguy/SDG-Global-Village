import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import pandas as pd

df = pd.read_csv('map/country_codes.csv')

data = [ dict(
        type = 'choropleth',
        locations = df['CODE'],
        z = np.ones(len(df)),
        text = df['COUNTRY'],
        colorscale = [[0,"rgb(5, 10, 172)"],
            [0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],
            [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],
            [1,"rgb(220, 220, 220)"]],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        showscale = False,
        hoverinfo = "text"
      ) ]

layout = dict(
    title = 'Select a country:',
    geo = dict(
        showframe = False,
        showcoastlines = True,
        projection = dict(
            type = 'robinson'
        )
    )
)

world_map_fig = dict( data=data, layout=layout )
# graph = py.iplot( fig, validate=False, filename='d3-world-map')