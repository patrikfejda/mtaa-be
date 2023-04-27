from inspect import signature
from typing import Callable

from pydantic import BaseModel


def get_pydantic_parameter_type(func: Callable):
    for param in signature(func).parameters.values():
        if issubclass(param.annotation, BaseModel):
            return param.annotation
