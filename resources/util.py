import os
from typing import Any
import logging

logger = logging.getLogger(__name__)


def get_env(name: str, default: Any, _type: type = str):
    value_str = os.getenv(name, None)
    if value_str is None:
        logger.info(f"Environment variable {name} was not set. Using default value {default}.")
        return default
    try:
        return _type(value_str)
    except ValueError:
        logger.warning(f"Could not interpret {name} ({value_str}) as {_type}. Using default value of {default}.")
    return default
