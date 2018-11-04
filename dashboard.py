import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools


app = dash.Dash()

############# BOOTSTRAP
app.css.append_css({
    "external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
})

df = pd.read_csv("datasets/meteorite-landings.csv")
df.dropna(inplace = True)

found_meteorites = df.groupby('fall').get_group('Found')
fell_meteorites = df.groupby('fall').get_group('Fell')

discoveries_by_fall = df.groupby("fall", as_index=False)
mean_mass_by_fall= pd.DataFrame(discoveries_by_fall["mass"].agg(np.mean))

main_class_occurences = pd.DataFrame(df["recclass"].value_counts().head())

main_class_discoveries = df[(df["recclass"] == "L6") | (df["recclass"] == "H5") | (df["recclass"] == "H6") | (df["recclass"] == "H4") | (df["recclass"] == "L5")| (df["recclass"] == "LL5")]

discoveries_by_main_classes = main_class_discoveries.groupby("recclass", as_index=False)
mean_mass_by_main_class = pd.DataFrame(discoveries_by_main_classes.mass.agg(np.mean))

main_class_discoveries_since_1950 = main_class_discoveries[main_class_discoveries["year"] >= 1950]
discoveries_by_main_classes_since_1950 = main_class_discoveries_since_1950.groupby(["year", "recclass"], as_index=False)
mean_mass_by_main_classes_since_1950 = pd.DataFrame(discoveries_by_main_classes_since_1950.mass.agg(np.mean))

trace1 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "L6"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "L6"]["mass"],
    mode='markers',
    name='L6',
    yaxis='y1'
)
trace2 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H5"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H5"]["mass"],
    mode='markers',
    name='H5',
    yaxis='y1'
)
trace3 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H6"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H6"]["mass"],
    mode='markers',
    name='H6',
    yaxis='y1'
)
trace4 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H4"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "H4"]["mass"],
    mode='markers',
    name='H4',
    yaxis='y2'
)
trace5 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "L5"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "L5"]["mass"],
    mode='markers',
    name='L5',
    yaxis='y2'
)
trace6 = go.Scatter(
    x = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "LL5"]["year"],
    y = mean_mass_by_main_classes_since_1950[mean_mass_by_main_classes_since_1950["recclass"] == "LL5"]["mass"],
    mode='markers',
    name='LL5',
    yaxis='y2'
)

fig = tools.make_subplots(rows=2, cols=3, subplot_titles=('L6', 'H5', 'H6', 'H4', 'L5', 'LL5'),
                          shared_xaxes=True, shared_yaxes=True,
                          vertical_spacing=0.05)
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 1, 2)
fig.append_trace(trace3, 1, 3)
fig.append_trace(trace4, 2, 1)
fig.append_trace(trace5, 2, 2)
fig.append_trace(trace6, 2, 3)

fig['layout'].update(height=600, title='Meteorites mean mass discoveries since 1950 faceted by their class', yaxis1 = {'title' : 'Mean mass (in g)', 'type' : 'log'}, yaxis2 = {'title' : 'Mean mass (in g)', 'type' : 'log'})

colors = {
    'background': '#DBDBDB',
    'text': '#303030'
}

palette = ["rgba(255,51,51,1)", "rgba(51,153,255,1)", "rgba(51,255,51,1)", "rgba(255,153,51,1)", "rgba(153,51,255,1)", "rgba(160,160,160,1)"]

app.layout = html.Div(className='container-fluid', children=[
    html.Div(className='row', children=[
        html.Div(className='col-md-2', style={"height": "100vh", "background" : "#1d283a"}, children=[
            html.Div(className="collapse show", id="navbarToggleExternalContent", style={'height' : '100vh','width':'80%'}, children=[
                html.H4('Dashboard', className="text-white", style={'color':'white'}),
                html.Div([
                    dcc.Input(id='date-input', value='1800', type='text'),
                    dcc.Slider(
                        id='year-slider',
                        min=1000,
                        max=2020,
                        value=1800,
                        marks={str(year): str(year) for year in df['year'].unique()}
                    ),
                    dcc.Dropdown(
                        id = "map-drop",
                        options = [{"label": "All impacts map", "value": "validMap"}, {"label": "Heatmap", "value": "heatMap"}, {"label": "Clustered map", "value": "clusteredMap"}, {"label": "Found and seen falling map", "value": "foundSeenFallingMap"}, {"label": "Class map", "value": "classMap"}],
                        placeholder = "Select Map"
                    ),
                    dcc.Dropdown(
                        id = "left-plot-drop",
                        options = [{"label": "Discoveries over time", "value": "discoveriesHist"}, {"label": "Meteorites mass distribution", "value": "massHist"}, {"label": "Mean mass per type", "value": "meanMassPerFall"}, {"label": "Meteorites classes", "value": "classesHist"}, {"label": "Mass per year per class", "value": "meanMassPerYearClass"}],
                        placeholder = "Select Left graph"
                    )
                ])
            ])
        ]),
        html.Div(className='col-md-8 col-md-offset-1', style={"height": "100vh"}, children=[
            html.Div(id = "mapBox", className='row', style={"height": "50%"} , children=[
                html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/heatmap.html', 'r', encoding='utf8').read()),
            ]),
            html.Div(className='row', style={"height": "50%"}, children=[
                html.Div(id="left-plot", className='col-md-5', children=[
                    dcc.Graph(
                        id='graph1',
                        figure={
                            'data': [
                                go.Histogram(
                                    x=df[df["year"] >= 1800]['year'],
                                    xbins=dict(start=np.min(df['year']), size=10, end=2020)
                                ) 
                            ],
                            'layout': go.Layout(
                                title = 'Meteorite discoveries distribution since 1800',
                                xaxis={'title': 'Time (year)'},
                                yaxis={'title': 'Quantity of discoveries', 'type' : 'log'},
                            )
                        }
                    )
                ]),
                html.Div(className='col-md-5', children=[
                    dcc.Graph(
                        id="graph2",
                        figure={
                            'data': [
                                go.Histogram(
                                    x=found_meteorites[found_meteorites["year"] >= 1800]['year'],
                                    xbins=dict(start=np.min(df['year']), size=10, end=2020)
                                ) 
                            ],
                            'layout': go.Layout(
                                title = 'Found meteorites distribution since 1800',
                                xaxis={'title': 'Time (year)'},
                                yaxis={'title': 'Quantity of discoveries', 'type' : 'log'}
                            )
                        }
                    ),
                ]),
            ])
        ])
    ]),
    dcc.Graph(
        id="hist4",
        figure={
            'data': [
                go.Histogram(
                    x=fell_meteorites[fell_meteorites["year"] >= 1800]['year'],
                    xbins=dict(start=np.min(df['year']), size=10, end=2020)
                ) 
            ],
            'layout': go.Layout(
                title = 'Seen falling meteorites distribution since 1800',
                xaxis={'title': 'Time (year)'},
                yaxis={'title': 'Quantity of discoveries', 'type' : 'log'}
            )
        }
    ),
    dcc.Graph(
        id="hist7",
        figure={
            'data': [
                go.Bar(
                    x=mean_mass_by_main_class.recclass,
                    y=mean_mass_by_main_class.mass,
                    marker = {
                        'color' : palette
                    }
                ) 
            ],
            'layout': go.Layout(
                title='Meteorites mean mass according to their class',
                xaxis={'title': 'Meteorite class'},
                yaxis={'title': 'Mean mass (in g)', 'rangemode' : 'tozero'}
            )
        }
    ),
    dcc.Graph(
        id="hist8",
        figure={
            'data': [
                go.Box(
                    x = df[df['fall'] == "Fell"]["fall"],
                    y = df.mass,
                    fillcolor= palette[0],
                    marker = {
                        'color' : palette[0]
                    }
                ),
                go.Box(
                    x = df[df['fall'] == "Found"]["fall"],
                    y = df.mass,
                    fillcolor= palette[1],
                    marker = {
                        'color' : palette[1]
                    }
                )
            ],
            'layout': go.Layout(
                title='Meteorites mass according to the type of discovery',
                xaxis={'title': 'Type of discovery'},
                yaxis={'title': 'Mass (in g)', 'type' : 'log'}
            )
        }
    ) 
])

@app.callback(
    Output(component_id='mapBox',component_property='children'),
    [Input(component_id='map-drop', component_property='value')]
)
def update_map(map_value):
    if map_value == 'validMap':
        return html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/allImpactsOverTimeMap.html', 'r', encoding='utf8').read())
    elif map_value == 'heatMap':
        return html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/heatmap.html', 'r', encoding='utf8').read())
    elif map_value == 'clusteredMap':
        return html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/clusteredMap.html', 'r', encoding='utf8').read())
    elif map_value == 'foundSeenFallingMap':
        return html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/discoveryTypeMap.html', 'r', encoding='utf8').read())
    else:
        return html.Iframe(style={'height':'100%', 'width':'100%'}, srcDoc = open('html-maps/discoveryClassMap.html', 'r', encoding='utf8').read())

@app.callback(
    Output(component_id='left-plot',component_property='children'),
    [Input(component_id='left-plot-drop', component_property='value')]
)

def update_left_plot(left_plot_value):
    if left_plot_value == 'discoveriesHist':
        return {
            dcc.Graph(
                figure={
                    'data': [
                        go.Histogram(
                            x=df[df["year"] >= 1800]['year'],
                            xbins=dict(start=np.min(df['year']), size=10, end=2020)
                        ) 
                    ],
                    'layout': go.Layout(
                        title = 'Meteorite discoveries distribution since 1800',
                        xaxis={'title': 'Time (year)'},
                        yaxis={'title': 'Quantity of discoveries', 'type' : 'log'},
                    )
                }
            )
        }
    elif left_plot_value == 'massHist':
        return {
            dcc.Graph(
                figure={
                    'data': [
                        go.Histogram(
                            x=df['mass'],
                            xbins=dict(start=np.min(df['mass']), size=100, end=10000)
                        ) 
                    ],
                    'layout': go.Layout(
                        title='Meteorite mass distribution',
                        xaxis={'title': 'Mass (in g)'},
                        yaxis={'title' : 'Quantity of meteorites', 'type' : 'log'}
                    )
                }
            )
        }
    elif left_plot_value == 'meanMassPerFall':
        return {
            dcc.Graph(
                figure={
                    'data': [
                        go.Bar(
                            x=mean_mass_by_fall.fall,
                            y=mean_mass_by_fall.mass,
                            marker = {
                                'color' : palette
                            }
                        ) 
                    ],
                    'layout': go.Layout(
                        title='Mean mass in terms of type of discovery',
                        xaxis={'title': 'Type of discovery'},
                        yaxis={'title' : 'Mean mass (in g)', 'rangemode' : 'tozero'}
                    )
                }
            )
        }
    elif left_plot_value == 'classesHist':
        return {
            dcc.Graph(
                figure={
                    'data': [
                        go.Bar(
                            x=main_class_occurences.index.tolist(),
                            y=main_class_occurences.recclass,
                            marker = {
                                'color' : palette
                            }
                        ) 
                    ],
                    'layout': go.Layout(
                        title='Six main meteorites class frequency',
                        xaxis={'title': 'Class of meteorite'},
                        yaxis={'title': 'Quantity of meteorites', 'rangemode' : 'tozero'}
                    )
                }
            )
        }
    else:
        return {
            dcc.Graph(
                figure = fig
            )
        }

if __name__ == '__main__':
   app.run_server(debug=True)