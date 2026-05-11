"""Unit tests for the calculator module."""

import pytest
from calculator import add, subtract, multiply, divide


class TestAdd:
    def test_positive_numbers(self):
        assert add(2, 3) == 5

    def test_negative_numbers(self):
        assert add(-1, -2) == -3

    def test_mixed_sign(self):
        assert add(-5, 10) == 5

    def test_floats(self):
        assert add(1.5, 2.5) == 4.0

    def test_zero(self):
        assert add(0, 0) == 0

    def test_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000


class TestSubtract:
    def test_basic(self):
        assert subtract(10, 3) == 7

    def test_negative_result(self):
        assert subtract(3, 10) == -7

    def test_zero(self):
        assert subtract(5, 5) == 0

    def test_floats(self):
        assert subtract(5.5, 2.2) == pytest.approx(3.3)

    def test_negative_subtrahend(self):
        assert subtract(5, -3) == 8


class TestMultiply:
    def test_basic(self):
        assert multiply(3, 4) == 12

    def test_by_zero(self):
        assert multiply(5, 0) == 0

    def test_negative(self):
        assert multiply(-3, 4) == -12

    def test_two_negatives(self):
        assert multiply(-3, -4) == 12

    def test_floats(self):
        assert multiply(2.5, 4.0) == 10.0


class TestDivide:
    def test_basic(self):
        assert divide(10, 2) == 5.0

    def test_float_result(self):
        assert divide(1, 3) == pytest.approx(1 / 3)

    def test_negative_dividend(self):
        assert divide(-10, 2) == -5.0

    def test_negative_divisor(self):
        assert divide(10, -2) == -5.0

    def test_both_negative(self):
        assert divide(-10, -2) == 5.0

    def test_divide_by_zero_raises(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_zero_numerator(self):
        assert divide(0, 5) == 0.0
