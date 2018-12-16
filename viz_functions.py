import pandas as pd


def get_total_seconds_series(timeseries):
    return 3600*timeseries.dt.hour + \
           60*timeseries.dt.minute + \
           timeseries.dt.second


def get_total_seconds_timestamp(timeseries):
    return 3600*timeseries.hour + \
           60*timeseries.minute + \
           timeseries.second


def get_data_within_time(min_time, max_time, df):
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
    time_diff = (max(df_filtered['time']) - min(df_filtered['time'])).total_seconds()

    return sum(df_filtered['count'])/max((time_diff/60), 1)


def get_typing_speed_over_time(df_filtered):
    """
    get data on typing speed over time
    :param df_filtered:
    :return:
    """
    # TODO
    
    pass


def get_character_sum(df_filtered):
    """
    get sum of typing specific characters
    """
    characters = sorted(df_filtered['character'].unique())
    counts = []
    for character in characters:
        counts.append(sum(df_filtered.loc[
                              df_filtered['character'] == character, 'counts']))

    return characters, counts
