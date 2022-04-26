from lazilypy import Lazy

from conftest import (
    get_lazy,
    lazy_created_and_not_started,
    lazy_builder_called_and_instance_started,
)


def test_addition():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int + 2 == 3
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 + lazy_int == 3
    lazy_builder_called_and_instance_started(lazy_int)

    assert get_lazy(int, 1) + get_lazy(int, 1) == 2


def test_concat():
    lazy_one = get_lazy(str, "one")
    lazy_created_and_not_started(lazy_one)
    assert lazy_one + "two" == "onetwo"
    lazy_builder_called_and_instance_started(lazy_one)

    lazy_two = get_lazy(str, "two")
    lazy_created_and_not_started(lazy_two)
    assert "one" + lazy_two == "onetwo"
    lazy_builder_called_and_instance_started(lazy_two)

    assert get_lazy(str, "one") + get_lazy(str, "two") == "onetwo"


def test_contains():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int in [2]) == (1 in [2])
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_list = get_lazy(list, [1, 2])
    lazy_created_and_not_started(lazy_list)
    print(lazy_list)
    assert (1 in lazy_list) == (1 in [1, 2])
    lazy_builder_called_and_instance_started(lazy_list)


def test_true_div():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int / 2 == 1 / 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 / lazy_int == 2 / 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_floor_div():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int // 2 == 1 // 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 // lazy_int == 2 // 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_and():
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


def test_bitwise_xor():
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


def test_bitwise_inversion():
    lazy_int: int | Lazy = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert ~lazy_int == ~1
    lazy_builder_called_and_instance_started(lazy_int)


def test_bitwise_or():
    lazy_int: int | Lazy = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int | 2 == 1 | 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 | lazy_int == 2 | 1
    assert 2 | lazy_int == 3
    lazy_builder_called_and_instance_started(lazy_int)


def test_power():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int**2 == 1**2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2**lazy_int == 2**1
    lazy_builder_called_and_instance_started(lazy_int)


def test_left_shift():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int << 2 == 1 << 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 << lazy_int == 2 << 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_modulo():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int % 2 == 1 % 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 % lazy_int == 2 % 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_multiplication():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int * 2 == 1 * 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 * lazy_int == 2 * 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_negation():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert -lazy_int == -1
    lazy_builder_called_and_instance_started(lazy_int)


def test_right_shift():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int >> 2 == 1 >> 2
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 >> lazy_int == 2 >> 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_subtraction():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert lazy_int - 2 == -1
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert 2 - lazy_int == 1
    lazy_builder_called_and_instance_started(lazy_int)


def test_less():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int < 2) == (1 < 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 < lazy_int) == (2 < 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_less_or_equal():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int <= 2) == (1 <= 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 <= lazy_int) == (2 <= 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_equal():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int == 2) == (1 == 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 == lazy_int) == (2 == 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_not_equal():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int != 2) == (1 != 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 != lazy_int) == (2 != 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_greater_or_equal():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int > 2) == (1 > 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 > lazy_int) == (2 > 1)
    lazy_builder_called_and_instance_started(lazy_int)


def test_greater():
    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (lazy_int > 2) == (1 > 2)
    lazy_builder_called_and_instance_started(lazy_int)

    lazy_int = get_lazy(int, 1)
    lazy_created_and_not_started(lazy_int)
    assert (2 > lazy_int) == (2 > 1)
    lazy_builder_called_and_instance_started(lazy_int)
