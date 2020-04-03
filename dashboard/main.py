from collections import defaultdict
from datetime import datetime


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output

from sources import Covid19Data

covid19 = Covid19Data()

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/kgantsov/pen/jOPROez.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#1c1d22',
    'text': '#7FDBFF'
}

app.layout = html.Div(className="layout", children=[

    html.Div(className="row", style={'backgroundColor': colors['background']}, children=[
        html.Div(className="chart-container twelwe columns", style={'backgroundColor': colors['background']}, children=[
            dcc.Dropdown(
                id='country-dropdown',
                options=[
                    {'label': covid19.countries_map[x[0]], 'value': x[0]}
                    for x in covid19.latest_total[::-1]
                ],
                value=[x[0] for x in covid19.latest_top[-5:]],
                multi=True
            ),
            dcc.RadioItems(
                id='type-radio',
                options=[
                    {'label': 'Confirmed', 'value': 'confirmed'},
                    {'label': 'Died', 'value': 'deaths'},
                    {'label': 'Recovered', 'value': 'recovered'}],
                value='confirmed',
            ),
            dcc.RangeSlider(
                id='dates-range-slider',
                min=0,
                max=len(covid19.dates) - 1,
                marks={
                    i: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %-d')
                    for i, x in enumerate(covid19.dates) if i % 5 == 0
                },
                value=[0, len(covid19.dates) - 1],
            ),
        ]),
    ]),

    html.Div(className="row", children=[
        html.Div(className="chart-container six columns", style={'backgroundColor': colors['background']}, children=[
            html.H1(
                children='Hello Dash',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),

            html.Div(children='Dash: A web application framework for Python.', style={
                'textAlign': 'center',
                'color': colors['text']
            }),

            dcc.Graph(
                id='example-graph-1',
                figure={
                    'data': [
                        {
                            'x': [x[0] for x in covid19.latest_top],
                            'y': [x[1]['confirmed'] for x in covid19.latest_top],
                            'type': 'bar',
                            'name': 'confirmed'
                        },
                        {
                            'x': [x[0] for x in covid19.latest_top],
                            'y': [x[1]['deaths'] for x in covid19.latest_top],
                            'type': 'bar',
                            'name': 'deaths'
                        },
                        {
                            'x': [x[0] for x in covid19.latest_top],
                            'y': [x[1]['recovered'] for x in covid19.latest_top],
                            'type': 'bar',
                            'name': 'recovered'
                        },
                    ],
                    'layout': {
                        # 'xaxis': {'title': 'Dates'},
                        # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                        # 'yaxis': {'title': 'Sick people'},
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            )
        ]),

        html.Div(className="chart-container six columns", style={'backgroundColor': colors['background']}, children=[
            html.H1(
                children='Hello Dash',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),

            html.Div(children='Dash: A web application framework for Python.', style={
                'textAlign': 'center',
                'color': colors['text']
            }),

            dcc.Graph(
                id='new-by-country',
                figure={
                    'data': [
                        # {
                        #     'x': list(covid19.locations_map['UA']['timelines']['confirmed']['timeline'].keys()),
                        #     'y': list(covid19.locations_map['UA']['timelines']['confirmed']['timeline'].values()),
                        #     'type': 'bar',
                        #     'name': 'Ukraine'
                        # },
                        # {
                        #     'x': list(covid19.locations_map['SE']['timelines']['confirmed']['timeline'].keys()),
                        #     'y': list(covid19.locations_map['SE']['timelines']['confirmed']['timeline'].values()),
                        #     'type': 'bar',
                        #     'name': 'Sweden'
                        # },
                        # {
                        #     'x': list(covid19.locations_map['IT']['timelines']['confirmed']['timeline'].keys()),
                        #     'y': list(covid19.locations_map['IT']['timelines']['confirmed']['timeline'].values()),
                        #     'type': 'bar',
                        #     'name': 'Italy'
                        # },
                    ],
                    'layout': {
                        'xaxis': {'title': 'Dates'},
                        # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                        'yaxis': {'title': 'Number of people'},
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            )
        ]),

    ]),

    html.Div(className="row", children=[
        html.Div(className="chart-container twelve columns", style={'backgroundColor': colors['background']}, children=[
            dcc.Graph(
                id='by-country',
                figure={
                    'data': [],
                    'layout': {
                        'xaxis': {'title': 'Dates'},
                        # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                        'yaxis': {'title': 'Sick people'},
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            ),
        ]),
    ]),
])

@app.callback(
    Output('by-country', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('type-radio', 'value'),
     Input('dates-range-slider', 'value')])
def update_new_stats_graph(countries, _type, dates_range):
    country_total = covid19.get_history_data(
        countries=countries,
        _type=_type,
        start=dates_range[0], 
        end=dates_range[1] + 1, 
    )

    return {
        'data': [
            {
                'x': list(data.keys()),
                'y': [x[_type] for x in data.values()],
                'type': 'line',
                'name': covid19.countries_map[c]
            } for c, data in country_total.items()
        ],
        'layout': {
            'yaxis': {'title': _type.title() if _type else ''},
            # 'yaxis': {'title': 'Sick people', 'type': 'log'},
            # 'yaxis': {'title': },
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }


@app.callback(
    Output('new-by-country', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('type-radio', 'value'),
     Input('dates-range-slider', 'value')])
def update_total_stats_graph(countries, _type, dates_range):
    country_total = covid19.get_history_data(
        countries=countries,
        _type=_type,
        start=dates_range[0], 
        end=dates_range[1] + 1, 
    )

    return {
        'data': [
            {
                'x': list(data.keys()),
                'y': [x[_type + '_new'] for x in data.values()],
                'type': 'line',
                'name': covid19.countries_map[c]
            } for c, data in country_total.items()
        ],
        'layout': {
            'yaxis': {'title': _type.title() if _type else ''},
            # 'yaxis': {'title': 'Sick people', 'type': 'log'},
            # 'yaxis': {'title': },
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }

if __name__ == '__main__':
    # http://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=UA&timelines=true
    # https://github.com/samayo/country-json/blob/master/src/country-by-population.json
    app.run_server(debug=True)