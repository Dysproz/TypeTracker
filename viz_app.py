import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from viz_functions import *
import plotly.graph_objs as go

data = DataHolder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        # Timeframe
        html.Div([
            html.H3(children='Pick the time frame'),

            html.H4(children='Pick the date'),

            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=dt.now(),
                end_date=dt.now()
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
                    value='00:00:00',
                    n_submit=0
                ),

                html.H6(children='To: '),

                dcc.Input(
                    id='time-to',
                    type='time',
                    placeholder='HH:MM:SS',
                    value='23:59:59',
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
                    get_average_typing_speed_overall(get_data_within_time(data.data))
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
        )],
        'layout': {
            'xaxis': {'title': 'Time'},
            'yaxis': {'title': 'CPM'}

        }
    }


def create_character_barchart(data_in, min_time, max_time, axist_type=[], title=[]):
    x, y = get_character_sum(
                get_data_within_time(data_in, min_time=min_time, max_time=max_time))
    return{
        'data': [go.Bar(
            x=x,
            y=y,
            text=x,
            textposition='auto',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            opacity=0.6
        )],
        'layout': {
            'xaxis': {'title': 'Character / function',
                      'showticklabels': False},
            'yaxis': {'title': 'Usage'}

        }
    }


@app.callback(
    Output('selected-date', 'children'),
    [Input('date-submit-button', 'n_clicks')],
    [State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')])
def update_date(n_clicks, start_date, end_date):
    start_date = dt.strptime(str(start_date.split()[0]), '%Y-%m-%d')
    end_date = dt.strptime(str(end_date.split()[0]), '%Y-%m-%d')
    data.set_data_ranges(start_date, end_date)
    return u'Selected date range: {start} - {end}'.format(start=str(start_date).split()[0],
                                                          end=str(end_date).split()[0])


@app.callback(
    Output('selected-time', 'children'),
    [Input('time-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_time(n_clicks, time_from, time_to):
    # TODO: add restraints on the min and max range and handle the errors
    return u'Analysis between {} and {}'.format(time_from, time_to)


@app.callback(
    Output('typing-speed-timeseries', 'figure'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_typing_timesteries_typing_speed(t_n_clicks, d_n_clicks, time_from, time_to):
    return create_typing_timeseries(data.data, min_time=time_from, max_time=time_to)


@app.callback(
    Output('character-use', 'figure'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_typing_timesteries_character_use(t_n_clicks, d_n_clicks, time_from, time_to):
    return create_character_barchart(data.data, min_time=time_from, max_time=time_to)


if __name__ == '__main__':
    app.run_server(debug=True)
