"""
This is a boilerplate pipeline 'data_science_fcst'
generated using Kedro 0.18.2
"""
import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.models import LightGBMModel
from darts.utils.model_selection import train_test_split
from darts.metrics.metrics import smape


def add_upgini_features(data_df: pd.DataFrame):
    pass


def split_train_test_data(data_df: pd.DataFrame):
    ts_data = TimeSeries.from_dataframe(data_df, time_col='datetime', value_cols=data_df.columns.drop('datetime'),
                                        fill_missing_dates=True, fillna_value=np.nan)
    train, test = train_test_split(ts_data, test_size=0.05)
    return train.pd_dataframe().reset_index(), test.pd_dataframe().reset_index()


def train_model(train: pd.DataFrame, test: pd.DataFrame):
    train = TimeSeries.from_dataframe(train, time_col='datetime', value_cols=train.columns.drop('datetime'),
                                      fill_missing_dates=True, fillna_value=np.nan)
    test = TimeSeries.from_dataframe(test, time_col='datetime', value_cols=test.columns.drop('datetime'),
                                     fill_missing_dates=True, fillna_value=np.nan)
    train_target = train['generation (w)']
    test_target = test['generation (w)']
    covariate_cols = train.columns.drop('generation (w)').tolist()
    add_encoders = {
        'cyclic': {'future': ['month', 'hour', 'dayofweek']},
        'datetime_attribute': {'future': ['hour', 'dayofweek']},
    }
    lgb_model = LightGBMModel(lags_past_covariates=24 * 7 * 12, lags=24 * 7 * 12, output_chunk_length=12 * 24, verbosity=2)
    lgb_model.fit(train_target, past_covariates=train[covariate_cols], verbose=True)
    return lgb_model


def evaluate_model(model: LightGBMModel, train: pd.DataFrame, test: pd.DataFrame) -> None:
    test = TimeSeries.from_dataframe(train, time_col='datetime', value_cols=train.columns.drop('datetime'),
                                     fill_missing_dates=True, fillna_value=np.nan)
    test = TimeSeries.from_dataframe(test, time_col='datetime', value_cols=test.columns.drop('datetime'),
                                     fill_missing_dates=True, fillna_value=np.nan)
    covariate_cols = test.columns.drop('generation (w)').tolist()
    test_target = test['generation (w)']
    preds = model.predict(n=12*24, past_covariates=train[covariate_cols].append(test[covariate_cols]))
    model_smape = smape(actual_series=test_target, pred_series=preds)
    print("Model SMAPE -> {}".format(model_smape))


