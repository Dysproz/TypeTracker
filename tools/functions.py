import pandas as pd
from datetime import datetime
import os


class DataHolder:
    def __init__(self):
        self.set_data_ranges(datetime.strptime('2018-12-16', '%Y-%m-%d'),
                             datetime.strptime('2018-12-15', '%Y-%m-%d'))
        self.set_time_ranges('00:00:00', '23:59:59')

    def get_data(self, start, end):
        path = './data'
        files = [i for i in os.listdir(path) if i.startswith('typer_')]
        files_dates = []
        for file in files:
            file_date = file[file.index('typer_')+len('typer_'):file.index('.csv')]
            files_dates.append(datetime.strptime(file_date, '%Y-%m-%d'))
        selected_dates = []
        for date in files_dates:
            if date >= start and date <= end:
                selected_dates.append('data/typer_{date}.csv'.format(date=date.strftime('%Y-%m-%d')))
        date_list = []
        for date in selected_dates:
            date_list.append(pd.read_csv(date, header=None))
        try:
            data = pd.concat(date_list, sort=True)
            data.columns = ['time', 'character', 'counts', 'type']
        except (UnboundLocalError, ValueError):
            data = pd.DataFrame(columns=['time', 'character', 'counts', 'type'])
        data['time'] = pd.to_datetime(data['time'])
        return data

    def set_time_ranges(self, time_from, time_to):
        self.time_from = time_from
        self.time_to = time_to

    def set_data_ranges(self, start, end):
        if isinstance(start, basestring):
            start = datetime.strptime(str(start.split()[0]), '%Y-%m-%d')
        if isinstance(end, basestring):
            end = datetime.strptime(str(end.split()[0]), '%Y-%m-%d')
        self.start_date = start
        self.end_date = end

    def get_data_within_time(self):
        total_min = self.get_total_seconds_timestamp(pd.to_datetime(self.time_from))
        total_max = self.get_total_seconds_timestamp(pd.to_datetime(self.time_to))
        df_seconds = self.get_total_seconds_series(self.data['time'])
        result = self.data.loc[(df_seconds >= total_min) & (df_seconds <= total_max), :]
        return result

    @property
    def data(self):
        return self.get_data(self.start_date, self.end_date)

    @staticmethod
    def get_total_seconds_timestamp(timeseries):
        return 3600*timeseries.hour + \
               60*timeseries.minute + \
               timeseries.second

    @staticmethod
    def get_total_seconds_series(timeseries):
        return 3600*timeseries.dt.hour + \
               60*timeseries.dt.minute + \
               timeseries.dt.second


def proper_timestamp(time):
    time = int(time)
    time_formated = datetime.fromtimestamp(time // 1000000000)
    return time_formated


def get_average_typing_speed_overall(data):
    try:
        time_diff = (max(data['time']) - min(data['time'])).total_seconds()
    except ValueError:
        time_diff = 0
        return 0
    return sum(data['counts'])/(time_diff/60.)


def get_percentage_usage_of_mouse_keyboard(data):
    total_records = float(sum(data['counts']))
    mouse_records = float(sum(data.loc[data['type'] == 'm', 'counts']))
    keyboard_records = float(sum(data.loc[data['type'] == 'k', 'counts']))
    if total_records != 0:
        return round(mouse_records/total_records*100, 2),\
               round(keyboard_records/total_records*100, 2)
    else:
        return 0, 0


def get_typing_speed_over_time(df_filtered):
    times = sorted(df_filtered['time'].unique())
    cpm = []
    times_formated = []
    for time in times:
        cpm.append(sum(df_filtered.loc[df_filtered['time'] == time, 'counts']))
        times_formated.append(proper_timestamp(time))
    return times_formated, cpm


def get_character_sum(df_filtered):
    characters = sorted(df_filtered['character'].unique())
    counts = []
    for character in characters:
        counts.append(sum(df_filtered.loc[df_filtered['character'] == character, 'counts']))
    return characters, counts
