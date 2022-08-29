"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.2
"""
import pandas as pd
from typing import Dict


def drop_unwanted_columns(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df.drop(columns=['Unnamed: 4'], inplace=True)
    return raw_df


def create_datetime_col(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df['datetime'] = raw_df['date'].astype(str) + ' ' + raw_df['time'].astype(str)
    raw_df['datetime'] = pd.to_datetime(raw_df['datetime'], format='%m/%d/%y %I:%M:%S %p')  # '%m/%d/%y %I:%M:%S %p'
    raw_df.drop(columns=['date', 'time'], inplace=True)
    return raw_df


def add_failures(raw_df: pd.DataFrame) -> pd.DataFrame:
    raw_df['failures'] = raw_df['generation (w)'].diff(-1).map(lambda x: 1 if abs(x) <= 0.01 * 7500 else 0)
    return raw_df
