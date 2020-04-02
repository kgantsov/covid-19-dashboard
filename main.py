from collections import defaultdict
from datetime import datetime


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output

import COVID19Py


total = defaultdict(lambda: defaultdict(int))

covid19 = COVID19Py.COVID19()
latest = covid19.getLatest()
locations = covid19.getLocations(timelines=True)
locations_map = {x['country_code']:x for x in locations}

countries_map = {}

for location in locations:
    countries_map[location['country_code']] = location['country']

    total[location['country_code']]['confirmed'] += location['latest']['confirmed']
    total[location['country_code']]['deaths'] += location['latest']['deaths']
    total[location['country_code']]['recovered'] += location['latest']['recovered']

latest_total = sorted(total.items(), key=lambda x: x[1]['confirmed'])
latest_top = latest_total[-20:]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://codepen.io/kgantsov/pen/jOPROez.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#1c1d22',
    'text': '#7FDBFF'
}

dates = list(locations_map['US']['timelines']['confirmed']['timeline'].keys())
print('±±±±±', dates, dates[0], dates[-1])

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

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
                    {'x': [x[0] for x in latest_top], 'y': [x[1]['confirmed'] for x in latest_top], 'type': 'bar', 'name': 'confirmed'},
                    {'x': [x[0] for x in latest_top], 'y': [x[1]['deaths'] for x in latest_top], 'type': 'bar', 'name': 'deaths'},
                    {'x': [x[0] for x in latest_top], 'y': [x[1]['recovered'] for x in latest_top], 'type': 'bar', 'name': 'recovered'},
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
            id='example-graph-2',
            figure={
                'data': [
                    {'x': list(locations_map['UA']['timelines']['confirmed']['timeline'].keys()), 'y': list(locations_map['UA']['timelines']['confirmed']['timeline'].values()), 'type': 'bar', 'name': 'Ukraine'},
                    {'x': list(locations_map['SE']['timelines']['confirmed']['timeline'].keys()), 'y': list(locations_map['SE']['timelines']['confirmed']['timeline'].values()), 'type': 'bar', 'name': 'Sweden'},
                    {'x': list(locations_map['IT']['timelines']['confirmed']['timeline'].keys()), 'y': list(locations_map['IT']['timelines']['confirmed']['timeline'].values()), 'type': 'bar', 'name': 'Italy'},
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

    html.Div(className="chart-container twelve columns", style={'backgroundColor': colors['background']}, children=[
        html.Div(style={'backgroundColor': colors['background']}, children=[
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': countries_map[x[0]], 'value': x[0]} for x in latest_total[::-1]],
                value=[x[0] for x in latest_top[-5:]],
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
                max=len(dates) - 1,
                marks={i: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').strftime('%b %-d') for i, x in enumerate(dates) if i % 5 == 0},
                value=[0, len(dates) - 1],
            ),
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
        ])
    ])
])

# print(';;;;;;;===', locations_map['US']['timelines']['confirmed']['timeline'])

@app.callback(
    Output('by-country', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('type-radio', 'value'),
     Input('dates-range-slider', 'value')])
def update_graph(countries, _type, dates_range):
    country_total = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for country in countries:
        # country_locations = covid19.getLocationByCountryCode(country, timelines=True)
        country_locations = [x for x in locations if x['country_code'] == country]

        for location in country_locations:
            for key, timeline in location['timelines'].items():
                # [dates_range[0]:dates_range[1]]
                items = list(timeline['timeline'].items())[dates_range[0]:dates_range[1]+1]
                for date, cnt in items:
                    country_total[location['country_code']][date][key] += cnt
        
    # print('......')
    # print(country_total)
    # print('......')

    return {
        'data': [
            {
                'x': list(data.keys()),
                'y': [x[_type] for x in data.values()],
                'type': 'line',
                'name': countries_map[c]
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
    app.run_server(debug=True)