import dash
from dash.dependencies import Input, Output, State
import tools.functions as functions
import tools.app_callbacks as callbacks

data = functions.DataHolder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "TypeTracker"
app.layout = callbacks.get_layout()


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
