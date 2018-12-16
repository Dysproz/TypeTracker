import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from viz_functions import *
import plotly.graph_objs as go


data = pd.read_csv('test_data')
data.columns = ['time', 'character', 'counts']
data['time'] = pd.to_datetime(data['time'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        # Timeframe
        html.Div([
            html.H3(children='Pick the time frame'),

            html.H4(children='Pick the date'),

            dcc.DatePickerSingle(
                id='single-date-picker',
                min_date_allowed=dt(2018, 12, 16),  # TODO: add a function reading files and what are the min/ max dates
                max_date_allowed=dt(2018, 12, 16),
                initial_visible_month=dt.now(),
                date=dt.now().strftime("%Y-%m-%d")
            ),

            html.Button(id='date-submit-button', n_clicks=0, children='Submit'),

            html.Div(id='selected-date'),

            html.H4(children='Pick the time range'),

            # Time from to
            html.Div([

                html.H6(children='From: '),

                dcc.Input(
                    id='time-from',
                    type='time',
                    placeholder='HH:MM:SS',
                    n_submit=0
                ),

                html.H6(children='To: '),

                dcc.Input(
                    id='time-to',
                    type='time',
                    placeholder='HH:MM:SS',
                    n_submit=0
                ),

                html.Button(id='time-submit-button', n_clicks=0, children='Submit')

            ], style={'columnCount': 2}),

            html.Div(id='selected-time')
        ]),

        # Summary section
        html.Div([  # TODO: add callback functions to get average speed and mouse use
            html.H3(children='Summary'),

            html.Div(
                id='typing-speed-summary',
                children='Average typing speed: {: .2f} Characters Per Minute.'.format(
                    get_average_typing_speed_overall(get_data_within_time(data))
                )),
            # TODO: add info button

            html.Div(id='mouse-use-summary')
            # TODO: add info button
        ]),

        # graphs
        html.Div([
            html.Div([
                html.H4(children='Typing speed in CPM over time.'),

                dcc.Graph(
                    id='typing-speed-timeseries',
                )]),

            html.Div([
                html.H4(children='Character use within selected time.'),

                html.Div([
                    dcc.Graph(
                        id='character-use'
                    )
                ])
            ])

        ])

    ])
])


def create_typing_timeseries(data_in, min_time, max_time, axist_type=[], title=[]):
    x, y = get_typing_speed_over_time(
                get_data_within_time(data_in, min_time=min_time, max_time=max_time))
    return{
        'data': [go.Scatter(
            x=x,
            y=y,
            mode='lines+markers'
        )]
    }


def create_character_barchart(data_in, min_time, max_time, axist_type, title):
    x, y = get_character_sum(
                get_data_within_time(data_in, min_time=min_time, max_time=max_time))
    return{
        'data': [go.Bar(
            x=x,
            y=y,
        )]
    }


@app.callback(
    Output('selected-date', 'children'),
    [Input('date-submit-button', 'n_clicks')],
    [State('single-date-picker', 'date')])
def update_date(n_clicks, input_date):
    data =pd.read_csv('data/typer_{}.csv'.format(str(input_date)))
    data.columns = ['time', 'character', 'counts']
    data['time'] = pd.to_datetime(data['time'])

    return u'Selected date: {}'.format(str(input_date))


@app.callback(
    Output('selected-time', 'children'),
    [Input('time-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_time(n_clicks, time_from, time_to):
    # TODO: add restraints on the min and max range and handle the errors
    return u'Analysis between {} and {}'.format(time_from, time_to)


@app.callback(
    Output('typing-speed-timeseries', 'figure'),
    [Input('time-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_typing_timesteries(n_clicks, time_from, time_to):
    return create_typing_timeseries(data, min_time=time_from, max_time=time_to)


if __name__ == '__main__':
    app.run_server(debug=True)
