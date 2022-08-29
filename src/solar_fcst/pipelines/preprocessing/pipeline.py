"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from solar_fcst.pipelines.preprocessing.nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=drop_unwanted_columns,
            inputs="pv_data_raw",
            outputs="pv_data_drop_unwanted",
            name="drop_unwanted_columns"
        ),
        node(
            func=create_datetime_col,
            inputs="pv_data_drop_unwanted",
            outputs="pv_data_intermediate",
            name='create_date_time_col'
        ),
        node(
            func=add_failures,
            inputs="pv_data_intermediate",
            outputs="processed_raw_pv_data"
        )
    ])
