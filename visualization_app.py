import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
import tools.functions as functions
import tools.app_callbacks as callbacks

data = functions.DataHolder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div([
        # Date Selector
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

            # Time Selector
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

        html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Summary', value='summary-tab'),
                dcc.Tab(label='CPM graph', value='cpm-tab'),
                dcc.Tab(label='Character use', value='character-use-tab'),
                ]),
            html.Div(id='tabs-content')
        ])
    ])
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    return callbacks.tab_render(tab)


@app.callback(
    Output('typing-speed-summary', 'children'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks'),
     Input('refresh', 'n_clicks')],
)
def update_summary_cpm(d_n_clicks, t_n_clicks, refresh_click):
    return callbacks.create_summary_section_cpm(data)


@app.callback(
    Output('device-usage-summary', 'children'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks'),
     Input('refresh', 'n_clicks')],
)
def update_summary_device_usage(d_n_clicks, t_n_clicks, refresh_click):
    return callbacks.create_summary_section_device_percentage(data)


@app.callback(
    Output('selected-date', 'children'),
    [Input('date-submit-button', 'n_clicks')],
    [State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')])
def update_date(n_clicks, start_date, end_date):
    return callbacks.update_data_date_ranges(data, start_date, end_date)


@app.callback(
    Output('selected-time', 'children'),
    [Input('time-submit-button', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_time(n_clicks, time_from, time_to):
    return callbacks.update_data_time_ranges(data, time_from, time_to)


@app.callback(
    Output('typing-speed-timeseries', 'figure'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks'),
     Input('refresh', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_typing_timesteries_typing_speed(t_n_clicks, d_n_clicks, refresh_click, time_from, time_to):
    return callbacks.create_typing_timeseries(data=data)


@app.callback(
    Output('character-use', 'figure'),
    [Input('time-submit-button', 'n_clicks'),
     Input('date-submit-button', 'n_clicks'),
     Input('refresh', 'n_clicks')],
    [State('time-from', 'value'), State('time-to', 'value')])
def update_typing_timesteries_character_use(t_n_clicks, d_n_clicks, refresh_click, time_from, time_to):
    return callbacks.create_character_barchart(data)


if __name__ == '__main__':
    app.run_server(debug=True)
