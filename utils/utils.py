import pandas as pd
from datetime import datetime

def convert_to_ny_datetime(date):

    if isinstance(date, (str, datetime)):
        date = pd.Timestamp(date)
        if date.tz is None:
            date = date.tz_localize('UTC')
        return date.tz_convert('America/New_York')

    elif isinstance(date, pd.Timestamp):
        if date.tzinfo is None:
            date = date.tz_localize('UTC')
        return date.tz_convert('America/New_York')

    elif isinstance(date, pd.Series):
        date = pd.to_datetime(date)
        if date.dt.tz is None:
            date = date.dt.tz_localize('UTC')
        return date.dt.tz_convert('America/New_York')

    elif isinstance(date, pd.DatetimeIndex):
        if date.tz is None:
            date = date.tz_localize('UTC')
        return date.tz_convert('America/New_York')

    else:
        raise TypeError("Invalid Date input")
