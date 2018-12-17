import pandas as pd
from datetime import datetime
import sys
import os

def get_total_seconds_series(timeseries):
    return 3600*timeseries.dt.hour + \
           60*timeseries.dt.minute + \
           timeseries.dt.second


def get_total_seconds_timestamp(timeseries):
    return 3600*timeseries.hour + \
           60*timeseries.minute + \
           timeseries.second

def proper_timestamp(time):
    time = int(time)
    time_formated = datetime.fromtimestamp(time // 1000000000)
    return time_formated

def get_data_within_time(df, min_time='00:00:00', max_time='23:59:59'):
    """
    get all data within specified time
    """
    total_min = get_total_seconds_timestamp(pd.to_datetime(min_time))
    total_max = get_total_seconds_timestamp(pd.to_datetime(max_time))
    df_seconds = get_total_seconds_series(df['time'])
    return df.loc[(df_seconds >= total_min) & (df_seconds <= total_max), :]


def get_average_typing_speed_overall(df_filtered):
    """
    calculate average typing speed of all characters in characters per minute
    """
    time_diff = (max(df_filtered['time']) - min(df_filtered['time'])).total_seconds() + 60  # 60 is the 60 of gathering data

    return sum(df_filtered['counts'])/(time_diff/60.)


def get_typing_speed_over_time(df_filtered):
    """
    get data on typing speed over time
    :param df_filtered:
    :return:
    """
    times = sorted(df_filtered['time'].unique())
    cpm = []
    times_formated = []
    for time in times:
        cpm.append(sum(df_filtered.loc[df_filtered['time'] == time, 'counts']))
        times_formated.append(proper_timestamp(time))
    return times_formated, cpm


def get_character_sum(df_filtered):
    """
    get sum of typing specific characters
    """
    characters = sorted(df_filtered['character'].unique())
    counts = []
    for character in characters:
        counts.append(sum(df_filtered.loc[df_filtered['character'] == character, 'counts']))

    return characters, counts

def get_data_for_date_range(start, end):
    """
    Iterate through data filenames and get files that match date range
    """
    path = './data'
    files = [i for i in os.listdir(path) if i.startswith('typer_')]
    files_dates = []
    for file in files:
        file_date = file[file.index('typer_')+len('typer_'):file.index('.csv')]
        files_dates.append(datetime.strptime(file_date, '%Y-%m-%d'))
    selected_dates = []
    for date in files_dates:
        if date >= start and date <= end:
            selected_dates.append(date)
    data = pd.DataFrame(columns=['time', 'character', 'counts'])
    for date in selected_dates:
        data.append(pd.read_csv('data/typer_{d}.csv'.format(d=date.strftime('%Y-%m-%d'))))
    data['time'] = pd.to_datetime(data['time'])
    return data
