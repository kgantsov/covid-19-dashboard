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
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://codepen.io/kgantsov/pen/jOPROez.css?v=3'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#1c1d22',
    'text': '#7FDBFF'
}

app.layout = html.Div(className="layout", children=[

    html.Div(className="row", style={'backgroundColor': colors['background']}, children=[
        html.Div(className="twelwe columns", style={'backgroundColor': colors['background']}, children=[
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
                className='radio-buttons',
                options=[
                    {'label': 'Confirmed', 'value': 'confirmed'},
                    {'label': 'Died', 'value': 'deaths'},
                    # {'label': 'Recovered', 'value': 'recovered'}
                ],
                value='confirmed',
            ),
            dcc.RangeSlider(
                id='dates-range-slider',
                min=0,
                max=len(covid19.get_dates()) - 1,
                marks={
                    i: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %-d')
                    for i, x in enumerate(covid19.get_dates()) if i % 5 == 0
                },
                value=[0, len(covid19.get_dates()) - 1],
            ),
        ]),
    ]),

    html.Div(className="row", children=[
        html.Div(
            id='by-country-container',
            className="six columns",
            style={'backgroundColor': colors['background']},
            children=[]
        ),

        html.Div(
            id='new-by-country-container',
            className="six columns",
            style={'backgroundColor': colors['background']},
            children=[]
        ),

    ]),

    html.Div(className="row", children=[
        html.Div(
            id='rates-progress-by-country-container',
            className="six columns",
            style={'backgroundColor': colors['background']},
            children=[]
        ),
    ]),
])

@app.callback(
    Output('by-country-container', 'children'),
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

    if _type == 'deaths':
        help_text = 'died from COVID-19'
    elif _type == 'confirmed':
        help_text = 'confirmed with COVID-19'
    elif _type == 'recovered':
        help_text = 'fully recovered from COVID-19'

    return [
        html.H1(
            children=f'Total {_type.title()} cases',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(
            children=f'Total number of people that {help_text} since the start',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id='by-country',
            figure={
                'data': [
                    {
                        'x': list(data.keys()),
                        'y': [x[_type] for x in data.values()],
                        'type': 'line',
                        'name': covid19.countries_map[c]
                    } for c, data in country_total.items()
                ],
                'layout': {
                    # 'yaxis': {'title': _type.title() if _type else ''},
                    # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                    # 'yaxis': {'title': },
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        ),
    ]


@app.callback(
    Output('new-by-country-container', 'children'),
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

    if _type == 'deaths':
        help_text = 'died from COVID-19'
    elif _type == 'confirmed':
        help_text = 'confirmed with COVID-19'
    elif _type == 'recovered':
        help_text = 'fully recovered from COVID-19'

    return [
        html.H1(
            children=f'New {_type} cases',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(
            children=f'Number of people that {help_text} on a specific day',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id='new-by-country',
            figure={
                'data': [
                    {
                        'x': list(data.keys()),
                        'y': [x[_type + '_new'] for x in data.values()],
                        'type': 'line',
                        'name': covid19.countries_map[c]
                    } for c, data in country_total.items()
                ],
                'layout': {
                    # 'yaxis': {'title': _type.title() if _type else ''},
                    # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                    # 'yaxis': {'title': },
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
    ]


@app.callback(
    Output('rates-progress-by-country-container', 'children'),
    [Input('country-dropdown', 'value'),
     Input('type-radio', 'value'),
     Input('dates-range-slider', 'value')])
def update_rates_progress__stats_graph(countries, _type, dates_range):
    country_total = covid19.get_history_data(
        countries=countries,
        _type=_type,
        start=dates_range[0], 
        end=dates_range[1] + 1, 
    )

    if _type == 'deaths':
        help_text = 'died from COVID-19'
    elif _type == 'confirmed':
        help_text = 'confirmed with COVID-19'
    elif _type == 'recovered':
        help_text = 'fully recovered from COVID-19'

    return [
        html.H1(
            children=f'{_type.title()} rate by date',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(
            children=f'Number of people that {help_text} per 1 million people on a specific day',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id='rates-progress-by-country',
            figure={
                'data': [
                    {
                        'x': list(data.keys()),
                        'y': [covid19.calculate_rate(c, x[_type]) for x in data.values()],
                        'type': 'line',
                        'name': covid19.countries_map[c]
                    } for c, data in country_total.items()
                ],
                'layout': {
                    # 'yaxis': {'title': _type.title() if _type else ''},
                    # 'yaxis': {'title': 'Sick people', 'type': 'log'},
                    # 'yaxis': {'title': },
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        ),
    ]

if __name__ == '__main__':
    # http://coronavirus-tracker-api.herokuapp.com/v2/locations?country_code=UA&timelines=true
    # https://github.com/samayo/country-json/blob/master/src/country-by-population.json
    app.run_server(debug=True, host='0.0.0.0', port='8050')
