import statistics
import unittest
from collections import UserDict
from decimal import Decimal
from fractions import Fraction
from unittest.mock import patch

from calc.errors import CalcError
from calc.stats import _as_numeric_list, mean, median, variance


FUNCTIONS = (mean, median, variance)
VALIDATORS = (_as_numeric_list,) + FUNCTIONS


class SinglePassIterable:
    def __init__(self, values):
        self.values = values
        self.iterations = 0
        self.yielded = []

    def __iter__(self):
        self.iterations += 1
        if self.iterations > 1:
            raise AssertionError("input iterated more than once")
        return self._items()

    def _items(self):
        for value in self.values:
            self.yielded.append(value)
            yield value


class StatsTest(unittest.TestCase):
    def test_singleton(self):
        self.assertEqual(mean([5]), 5)
        self.assertEqual(median([5]), 5)
        self.assertEqual(variance([5]), 0)

    def test_unsorted_odd_length(self):
        self.assertEqual(mean([3, 1, 2]), 2)
        self.assertEqual(median([3, 1, 2]), 2)
        self.assertAlmostEqual(variance([3, 1, 2]), 2 / 3)

    def test_even_length_uses_population_variance(self):
        self.assertEqual(mean([4, 1, 3, 2]), 2.5)
        self.assertEqual(median([4, 1, 3, 2]), 2.5)
        self.assertEqual(variance([4, 1, 3, 2]), 1.25)

    def test_constant_values(self):
        self.assertEqual(mean([7, 7, 7]), 7)
        self.assertEqual(median([7, 7, 7]), 7)
        self.assertEqual(variance([7, 7, 7]), 0)

    def test_negative_values_and_zero(self):
        self.assertEqual(mean([-2, 0, 2]), 0)
        self.assertEqual(median([-2, 0, 2]), 0)
        self.assertAlmostEqual(variance([-2, 0, 2]), 8 / 3)

    def test_float_values(self):
        self.assertAlmostEqual(mean([0.1, 0.2, 0.3]), 0.2)
        self.assertAlmostEqual(median([0.1, 0.2, 0.3]), 0.2)
        self.assertAlmostEqual(variance([0.1, 0.2, 0.3]), 1 / 150)

    def test_mixed_ints_and_floats(self):
        self.assertEqual(mean([1, 2.0, 3]), 2)
        self.assertEqual(median([1, 2.0, 3]), 2)
        self.assertAlmostEqual(variance([1, 2.0, 3]), 2 / 3)

    def test_median_selects_middle_rather_than_mean(self):
        self.assertEqual(median([100, 1, 2]), 2)
        self.assertEqual(median([100, 1, 3, 2]), 2.5)

    def test_variance_avoids_catastrophic_cancellation(self):
        self.assertAlmostEqual(variance([1e12 + 1, 1e12 + 2, 1e12 + 3]), 2 / 3)

    def test_large_finite_mean_and_even_median_do_not_overflow(self):
        self.assertEqual(mean([1e308, 1e308]), 1e308)
        self.assertEqual(median([1e308, 1e308]), 1e308)

    def test_variance_overflow_raises_calc_error(self):
        with self.assertRaises(CalcError):
            variance([1e200, -1e200])

    def test_large_integers_are_valid(self):
        value = 10 ** 400
        self.assertEqual(mean([value, value]), value)
        self.assertEqual(median([value, value]), value)
        self.assertEqual(variance([value, value]), 0)

    def test_bools_are_numbers(self):
        self.assertAlmostEqual(mean([True, False, True]), 2 / 3)
        self.assertEqual(median([True, False, True]), 1)
        self.assertAlmostEqual(variance([True, False, True]), 2 / 9)

    def test_tuple_and_one_shot_iterator_inputs(self):
        for function, expected in ((mean, 2.5), (median, 2.5), (variance, 1.25)):
            for factory in (tuple, iter):
                with self.subTest(function=function.__name__, factory=factory.__name__):
                    values = factory([1, 2, 3, 4])
                    self.assertEqual(function(values), expected)

    def test_each_call_consumes_input_once(self):
        for function, expected in (
            (_as_numeric_list, [4, 1, 3, 2]),
            (mean, 2.5),
            (median, 2.5),
            (variance, 1.25),
        ):
            with self.subTest(function=function.__name__):
                values = SinglePassIterable([4, 1, 3, 2])
                self.assertEqual(function(values), expected)
                self.assertEqual(values.iterations, 1)
                self.assertEqual(values.yielded, [4, 1, 3, 2])

    def test_input_list_is_not_mutated(self):
        for function in VALIDATORS:
            with self.subTest(function=function.__name__):
                values = [3, 1, 2]
                function(values)
                self.assertEqual(values, [3, 1, 2])

    def test_helper_returns_independent_list(self):
        values = [3, 1, 2]
        snapshot = _as_numeric_list(values)
        self.assertIsInstance(snapshot, list)
        self.assertEqual(snapshot, values)
        self.assertIsNot(snapshot, values)
        snapshot.append(4)
        self.assertEqual(values, [3, 1, 2])

    def test_helper_normalizes_bools_without_mutating_input(self):
        values = [True, False, 2, 3.5]
        snapshot = _as_numeric_list(values)
        self.assertEqual(snapshot, [1, 0, 2, 3.5])
        self.assertIs(type(snapshot[0]), int)
        self.assertIs(type(snapshot[1]), int)
        self.assertIs(values[0], True)
        self.assertIs(values[1], False)

    def test_empty_inputs_raise_calc_error(self):
        for function in VALIDATORS:
            for factory in (list, tuple, lambda: iter(())):
                with self.subTest(function=function.__name__, factory=factory):
                    with self.assertRaises(CalcError):
                        function(factory())

    def test_exhausted_iterator_raises_calc_error(self):
        for function in VALIDATORS:
            with self.subTest(function=function.__name__):
                values = iter([1])
                next(values)
                with self.assertRaises(CalcError):
                    function(values)

    def test_non_iterables_raise_calc_error(self):
        for function in VALIDATORS:
            for values in (5, 1.5, None, True, object()):
                with self.subTest(function=function.__name__, values=values):
                    with self.assertRaises(CalcError):
                        function(values)

    def test_text_bytes_and_mappings_are_rejected(self):
        invalid_inputs = (
            "abc", "", b"ab", b"", bytearray(b"ab"), bytearray(),
            memoryview(b"ab"), memoryview(b""),
            {"a": 1}, {1: 2}, {}, UserDict({1: 2}),
        )
        for function in VALIDATORS:
            for values in invalid_inputs:
                with self.subTest(function=function.__name__, values=values):
                    with self.assertRaises(CalcError):
                        function(values)

    def test_non_numeric_and_non_finite_elements_raise_calc_error(self):
        invalid_elements = (
            "x", None, 1j, Decimal("1"), Fraction(1, 2),
            [], [1], (1,), {}, {1}, b"1",
            float("nan"), float("inf"), float("-inf"),
        )
        for function in VALIDATORS:
            for value in invalid_elements:
                for values in ([value], [1, value]):
                    with self.subTest(function=function.__name__, values=values):
                        with self.assertRaises(CalcError):
                            function(values)

    def test_median_rejects_strings_even_when_sortable(self):
        with self.assertRaises(CalcError):
            median(["c", "a", "b"])

    def test_iter_type_error_is_translated(self):
        class BadIterable:
            def __iter__(self):
                raise TypeError("cannot create iterator")

        for function in VALIDATORS:
            with self.subTest(function=function.__name__):
                with self.assertRaises(CalcError):
                    function(BadIterable())

    def test_other_iter_errors_propagate_unchanged(self):
        for function in VALIDATORS:
            for exception_type in (ValueError, RuntimeError, OverflowError):
                with self.subTest(function=function.__name__, error=exception_type):
                    error = exception_type("cannot create iterator")

                    class BadIterable:
                        def __iter__(self):
                            raise error

                    with self.assertRaises(exception_type) as caught:
                        function(BadIterable())
                    self.assertIs(caught.exception, error)

    def test_errors_during_iteration_propagate_unchanged(self):
        for function in VALIDATORS:
            for exception_type in (
                ValueError, TypeError, RuntimeError, OverflowError,
                statistics.StatisticsError,
            ):
                with self.subTest(function=function.__name__, error=exception_type):
                    error = exception_type("boom")

                    def values():
                        yield 1
                        raise error

                    with self.assertRaises(exception_type) as caught:
                        function(values())
                    self.assertIs(caught.exception, error)

    def test_statistics_overflow_and_statistics_error_are_translated(self):
        for function, operation in (
            (mean, "mean"), (median, "mean"), (variance, "pvariance"),
        ):
            for exception_type in (OverflowError, statistics.StatisticsError):
                with self.subTest(function=function.__name__, error=exception_type):
                    with patch(
                        "calc.stats.statistics." + operation,
                        side_effect=exception_type("out of range"),
                    ):
                        with self.assertRaises(CalcError):
                            function([1, 2])

    def test_non_finite_statistics_results_raise_calc_error(self):
        for function, operation in (
            (mean, "mean"), (median, "mean"), (variance, "pvariance"),
        ):
            for result in (float("inf"), float("-inf"), float("nan")):
                with self.subTest(function=function.__name__, result=result):
                    with patch("calc.stats.statistics." + operation, return_value=result):
                        with self.assertRaises(CalcError):
                            function([1, 2])

    def test_other_statistics_errors_propagate_unchanged(self):
        for function, operation in (
            (mean, "mean"), (median, "mean"), (variance, "pvariance"),
        ):
            for exception_type in (TypeError, ValueError, RuntimeError):
                with self.subTest(function=function.__name__, error=exception_type):
                    error = exception_type("unexpected error")
                    with patch("calc.stats.statistics." + operation, side_effect=error):
                        with self.assertRaises(exception_type) as caught:
                            function([1, 2])
                    self.assertIs(caught.exception, error)


if __name__ == "__main__":
    unittest.main()
