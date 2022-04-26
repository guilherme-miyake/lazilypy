from typing import TypeVar
from unittest.mock import MagicMock

from lazilypy import Lazy, logger

from lazilypy.defaults import supported_python_operators
from conftest import (
    get_lazy,
    lazy_created_and_not_started,
    lazy_builder_called_and_instance_started,
)


def test_addition_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int + 2 == 3
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 + lazy_int == 3
    lazy_builder_called_and_instance_started(lazy_int)


def test_concat_operator():
    lazy_one = get_lazy(str, "one")
    lazy_created_and_not_started(lazy_one)
    assert lazy_one + "two" == "onetwo"
    lazy_builder_called_and_instance_started(lazy_one)

    # TODO: Unsupported
    # lazy_two = get_lazy(str, "two")
    # print(type(lazy_two))
    # lazy_created_and_not_started(lazy_two)
    # assert "one" + lazy_two == "onetwo"
    # lazy_builder_called_and_instance_started(lazy_two)


def test_contains_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int in [2]) == (1 in [2])
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_list = get_lazy(list, [1, 2])
    lazy_created_and_not_started(lazy_list)
    print(lazy_list)
    assert (1 in lazy_list) == (1 in [1, 2])
    lazy_builder_called_and_instance_started(lazy_list)


def test_true_div_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int / 2 == 1 / 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 / lazy_int == 2 / 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_floor_div_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int // 2 == 1 // 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 // lazy_int == 2 // 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_and_operator():
    # TODO: Unsupported
    # lazy_int: int | Lazy = get_lazy(int, 1)
    # lazy_created_and_not_started(lazy_int)
    # assert lazy_int & 2 == 1 & 2
    # lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 & lazy_int == 2 & 1
    assert 2 & lazy_int == 0
    lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_xor_operator():
    lazy_int: int | Lazy = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int ^ 2 == 1 ^ 2
    assert lazy_int ^ 2 == 3
    lazy_builder_called_and_instance_started(lazy_int)

    # TODO: Unsupported
    # lazy_int = get_lazy(int, 1)
    # lazy_created_and_not_started(lazy_int)
    # assert 2 ^ lazy_int == 2 ^ 1
    # assert 2 ^ lazy_int == 3
    # lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_inversion_operator():
    # TODO: Unsupported
    lazy_int: int | Lazy = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert ~lazy_int == ~1
    lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_or_operator():
    lazy_int: int | Lazy = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int | 2 == 1 | 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 | lazy_int == 2 | 1
    assert 2 | lazy_int == 3
    lazy_builder_called_and_instance_started(lazy_int)


def test_power_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int**2 == 1**2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2**lazy_int == 2**1
    lazy_builder_called_and_instance_started(lazy_int)


def test_floor_mod_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int % 2 == 1 % 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 % lazy_int == 2 % 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_multiplication_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int * 2 == 1 * 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 * lazy_int == 2 * 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_greater_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int > 2) == (1 > 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 > lazy_int) == (2 > 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_lesser_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int < 2) == (1 < 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 < lazy_int) == (2 < 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_lesser_equal_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int <= 2) == (1 <= 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 <= lazy_int) == (2 <= 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_equal_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int == 2) == (1 == 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 == lazy_int) == (2 == 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_not_equal_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int != 2) == (1 != 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 != lazy_int) == (2 != 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_sub_operator():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int - 2 == -1
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 - lazy_int == 1
    lazy_builder_called_and_instance_started(lazy_int)
