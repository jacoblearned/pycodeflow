""" Pytest fixtures """
import os
import pytest
from pycodeflow import ENVIRONMENT_VARIABLES


@pytest.fixture(scope="function", autouse=True)
def clear_pycodeflow_env_vars():
    """ Remove any existing Pycodeflow env vars and reset them after test execution """

    existing_env_vars = set(ENVIRONMENT_VARIABLES) & set(os.environ.keys())
    env_var_cache = {env_var: os.environ.pop(env_var) for env_var in existing_env_vars}
    yield
    os.environ.update(env_var_cache)
