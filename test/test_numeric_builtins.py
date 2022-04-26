import math

from conftest import (
    get_lazy,
    lazy_created_and_not_started,
    lazy_builder_called_and_instance_started,
)


def test_abs():
    lazy_int = get_lazy(int, -1)
    lazy_created_and_not_started(lazy_int)
    assert abs(lazy_int) == abs(-1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_ceil():
    lazy_int = get_lazy(float, 1.3)
    lazy_created_and_not_started(lazy_int)
    assert math.ceil(lazy_int) == math.ceil(1.3)
    lazy_builder_called_and_instance_started(lazy_int)


def test_floor():
    lazy_int = get_lazy(float, 1.3)
    lazy_created_and_not_started(lazy_int)
    assert math.floor(lazy_int) == math.floor(1.3)
    lazy_builder_called_and_instance_started(lazy_int)


def test_int():
    lazy_int = get_lazy(float, 1.3)
    lazy_created_and_not_started(lazy_int)
    assert int(lazy_int) == int(1.3)
    lazy_builder_called_and_instance_started(lazy_int)


def test_float():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert float(lazy_int) == float(1)
    lazy_builder_called_and_instance_started(lazy_int)
