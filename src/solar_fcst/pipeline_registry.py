"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
import solar_fcst.pipelines.preprocessing.pipeline as pps
import solar_fcst.pipelines.data_science_fcst.pipeline as ds


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    preprocess_raw_pv_pipeline = pps.create_pipeline()
    data_science_pipeline = ds.create_pipeline()
    return {"__default__": preprocess_raw_pv_pipeline + data_science_pipeline,
            "preprocess_raw_pv": preprocess_raw_pv_pipeline}
