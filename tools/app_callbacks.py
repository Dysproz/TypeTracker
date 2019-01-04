from datetime import datetime as dt
import tools.functions as functions
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html


def get_layout():
    layout = html.Div([
                html.Div([
                    html.H1(children='TypeTracker', style={'text-align': 'center',
                                                           'font': 'helvetica',
                                                           'color': '#327DFF'}),

                    # Date Selector
                    html.Div([
                        html.H4(children='Pick the date'),

                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=dt.now(),
                            end_date=dt.now()
                        ),

                        html.Div([
                            html.Button(id='date-submit-button', n_clicks=0, children='Submit')
                            ], style={'padding': '10px'}),

                        html.Div(id='selected-date')
                    ], style={'width': '49%',
                              'display': 'inline-block',
                              'text-align': 'center',
                              'vertical-align': 'text-top'}),

                    # Time Selector
                    html.Div([
                        html.H4(children='Pick the time range'),
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
                            )], style={'columnCount': 2}),

                        html.Button(id='time-submit-button', n_clicks=0, children='Submit'),

                        html.Div(id='selected-time')
                        ], style={'width': '49%',
                                  'display': 'inline-block',
                                  'text-align': 'center',
                                  'vertical-align': 'text-top'}),

                    # Tabs
                    html.Div([
                        dcc.Tabs(id="tabs", value='summary-tab', children=[
                            dcc.Tab(label='Summary', value='summary-tab'),
                            dcc.Tab(label='CPM graph', value='cpm-tab'),
                            dcc.Tab(label='Character use', value='character-use-tab'),
                            ]),
                        html.Div(id='tabs-content')
                    ])
                ])
            ])
    return layout


def create_summary_section_cpm(data):
    return 'Average typing speed: {: .2f} Characters Per Minute.'.format(
           functions.get_average_typing_speed_overall(data.get_data_within_time()))


def create_summary_section_device_percentage(data):
    mouse, keyboard = functions.get_percentage_usage_of_mouse_keyboard(data.get_data_within_time())
    return 'Usage of keyboard: {keyboard}%.\n'\
           'Usage of mouse: {mouse}%.'.format(keyboard=keyboard, mouse=mouse)


def create_typing_timeseries(data, axist_type=[], title=[]):
    x, y = functions.get_typing_speed_over_time(data.get_data_within_time())
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


def create_character_barchart(data, axist_type=[], title=[]):
    x, y = functions.get_character_sum(data.get_data_within_time())
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


def update_data_date_ranges(data, start_date, end_date):
    start_date = dt.strptime(str(start_date.split()[0]), '%Y-%m-%d')
    end_date = dt.strptime(str(end_date.split()[0]), '%Y-%m-%d')
    data.set_data_ranges(start_date, end_date)
    return u'Selected date range: {start} - {end}'.format(start=str(start_date).split()[0],
                                                          end=str(end_date).split()[0])


def update_data_time_ranges(data, time_from, time_to):
    data.set_time_ranges(time_from=time_from, time_to=time_to)
    return u'Analysis between {} and {}'.format(time_from, time_to)


def tab_render(tab):
    if tab == 'summary-tab':
        return html.Div([
                    html.H3(children='Summary'),

                    html.Div(id='typing-speed-summary'),

                    html.Div(id='device-usage-summary'),

                    html.Button(id='refresh', n_clicks=0, children='Refresh'),
                ], style={'text-align': 'center'})

    elif tab == 'cpm-tab':
        return html.Div([
                    html.H4(children='Typing speed in CPM over time.'),

                    dcc.Graph(
                        id='typing-speed-timeseries',
                    ),

                    html.Button(id='refresh', n_clicks=0, children='Refresh')
                    ], style={'text-align': 'center'})

    elif tab == 'character-use-tab':
        return html.Div([
                    html.H4(children='Character use within selected time.'),

                    html.Div([
                        dcc.Graph(
                            id='character-use'
                        )
                    ]),

                    html.Button(id='refresh', n_clicks=0, children='Refresh')
                ], style={'text-align': 'center'})
