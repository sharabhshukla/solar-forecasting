"""
This is a boilerplate pipeline 'data_science_fcst'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from solar_fcst.pipelines.data_science_fcst.nodes import *


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=split_train_test_data,
            inputs="processed_raw_pv_data",
            outputs=["training_data", "testing_data"],
            name="train_test_data_split"
        ),
        node(
            func=train_model,
            inputs=["training_data","testing_data"],
            outputs="darts_model_lgb",
            name="model_training"
        ),
        node(
            func=evaluate_model,
            inputs=["darts_model_lgb", "testing_data"],
            outputs=[],
            name='model_evaluation'
        )
    ])
