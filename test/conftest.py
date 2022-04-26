from unittest.mock import MagicMock

import pytest
from typing import TypeVar, Type

from lazilypy import logger, Lazy

logger.setLevel(1)

_T = TypeVar("_T")


def get_lazy(cls: Type[_T], *default):
    lazy_int = Lazy(cls, *default)
    lazy_int._lazy_builder_ = MagicMock(return_value=cls(*default))  # type: ignore[operator]
    return lazy_int


def lazy_created_and_not_started(lazy_instance: Lazy):
    assert type(lazy_instance) == Lazy
    lazy_instance._lazy_builder_.assert_not_called()  # type: ignore[attr-defined]
    assert lazy_instance._lazy_ref_instance_ is None


def lazy_builder_called_and_instance_started(lazy_instance: Lazy):
    lazy_instance._lazy_builder_.assert_called_once()  # type: ignore[attr-defined]
    assert lazy_instance._lazy_ref_instance_ is not None
