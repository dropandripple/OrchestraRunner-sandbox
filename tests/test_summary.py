import re
import sys
import unittest
from collections import UserDict
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from calc.errors import CalcError
from calc.stats import mean, median, variance


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


class SummaryTest(unittest.TestCase):
    def setUp(self):
        from calc.summary import summary

        self.summary = summary

    def test_even_length_population_variance(self):
        self.assertEqual(
            self.summary([4, 1, 3, 2]),
            {"mean": 2.5, "median": 2.5, "variance": 1.25},
        )

    def test_singleton_and_constant_values(self):
        for values, expected in (
            ([5], {"mean": 5, "median": 5, "variance": 0}),
            ([7, 7, 7], {"mean": 7, "median": 7, "variance": 0}),
        ):
            with self.subTest(values=values):
                self.assertEqual(self.summary(values), expected)

    def test_odd_length_and_negative_values(self):
        for values, center, spread in (
            ([3, 1, 2], 2, 2 / 3),
            ([-2, 0, 2], 0, 8 / 3),
        ):
            with self.subTest(values=values):
                result = self.summary(values)
                self.assertEqual(result["mean"], center)
                self.assertEqual(result["median"], center)
                self.assertAlmostEqual(result["variance"], spread)

    def test_median_uses_middle_values(self):
        for values, expected in (([100, 1, 2], 2), ([100, 1, 3, 2], 2.5)):
            with self.subTest(values=values):
                self.assertEqual(self.summary(values)["median"], expected)

    def test_float_values_and_exact_keys(self):
        result = self.summary([0.1, 0.2, 0.3])
        self.assertIsInstance(result, dict)
        self.assertEqual(set(result), {"mean", "median", "variance"})
        self.assertAlmostEqual(result["mean"], 0.2)
        self.assertAlmostEqual(result["median"], 0.2)
        self.assertAlmostEqual(result["variance"], 1 / 150)

    def test_matches_individual_statistics(self):
        for values in (
            [5], [3, 1, 2], [4, 1, 3, 2], [7, 7, 7],
            [-2, 0, 2], [0.1, 0.2, 0.3],
        ):
            with self.subTest(values=values):
                self.assertEqual(
                    self.summary(values),
                    {"mean": mean(values), "median": median(values),
                     "variance": variance(values)},
                )

    def test_finite_iterable_inputs(self):
        for factory in (list, tuple, iter, lambda items: (x for x in items)):
            with self.subTest(factory=factory):
                self.assertEqual(
                    self.summary(factory([1, 2, 3, 4])),
                    self.summary([1, 2, 3, 4]),
                )
        self.assertEqual(
            self.summary(range(1, 5)),
            {"mean": 2.5, "median": 2.5, "variance": 1.25},
        )
        self.assertEqual(
            self.summary({1, 2, 3, 4}),
            {"mean": 2.5, "median": 2.5, "variance": 1.25},
        )

    def test_original_iterable_is_consumed_once(self):
        values = SinglePassIterable([4, 1, 3, 2])
        self.assertEqual(
            self.summary(values),
            {"mean": 2.5, "median": 2.5, "variance": 1.25},
        )
        self.assertEqual(values.iterations, 1)
        self.assertEqual(values.yielded, [4, 1, 3, 2])

    def test_input_is_unchanged_and_results_are_independent(self):
        values = [3, 1, 2]
        first = self.summary(values)
        second = self.summary(values)
        self.assertEqual(values, [3, 1, 2])
        self.assertIsNot(first, second)
        self.assertEqual(first, second)
        first["mean"] = -100
        first["extra"] = 1
        self.assertEqual(second, {"mean": 2, "median": 2, "variance": 2 / 3})

    def test_mixed_numbers_and_bools(self):
        result = self.summary([True, False, True])
        self.assertAlmostEqual(result["mean"], 2 / 3)
        self.assertEqual(result["median"], 1)
        self.assertAlmostEqual(result["variance"], 2 / 9)
        self.assertEqual(
            self.summary([1, 2.0, 3]),
            {"mean": 2, "median": 2, "variance": 2 / 3},
        )

    def test_large_finite_values_are_supported(self):
        for value in (1e308, 10 ** 400):
            with self.subTest(value=value):
                self.assertEqual(
                    self.summary([value, value]),
                    {"mean": value, "median": value, "variance": 0},
                )

    def test_empty_inputs_raise_calc_error(self):
        for factory in (list, tuple, lambda: iter(())):
            with self.subTest(factory=factory):
                with self.assertRaises(CalcError):
                    self.summary(factory())

    def test_non_iterable_inputs_raise_calc_error(self):
        for values in (None, 5, 1.5, True, object()):
            with self.subTest(values=values):
                with self.assertRaises(CalcError):
                    self.summary(values)

    def test_text_bytes_and_mappings_raise_calc_error(self):
        for values in (
            "123", "", b"12", b"", bytearray(b"ab"), bytearray(),
            memoryview(b"12"), memoryview(b""), {1: 2}, {}, UserDict({1: 2}),
        ):
            with self.subTest(values=values):
                with self.assertRaises(CalcError):
                    self.summary(values)

    def test_non_numeric_and_non_finite_elements_raise_calc_error(self):
        for value in (
            "x", None, 1j, Decimal("1"), Fraction(1, 2), [], {}, b"1",
            float("nan"), float("inf"), float("-inf"),
        ):
            for values in ([value], [1, value]):
                with self.subTest(values=values):
                    with self.assertRaises(CalcError):
                        self.summary(values)

    def test_variance_overflow_raises_calc_error(self):
        with self.assertRaises(CalcError):
            self.summary([1e200, -1e200])

    def test_uses_stats_functions_and_validator(self):
        from calc.stats import _as_numeric_list

        module = sys.modules["calc.summary"]
        for name, function in (
            ("_as_numeric_list", _as_numeric_list),
            ("mean", mean), ("median", median), ("variance", variance),
        ):
            with self.subTest(name=name):
                self.assertIs(getattr(module, name), function)

    def test_statistics_receive_the_same_validated_snapshot(self):
        module = sys.modules["calc.summary"]
        values = iter([3, 1, 2])
        snapshot = [3, 1, 2]
        with patch.object(module, "_as_numeric_list", return_value=snapshot) as validate, \
                patch.object(module, "mean", return_value=10) as mean_mock, \
                patch.object(module, "median", return_value=20) as median_mock, \
                patch.object(module, "variance", return_value=30) as variance_mock:
            self.assertEqual(
                self.summary(values), {"mean": 10, "median": 20, "variance": 30}
            )
        validate.assert_called_once_with(values)
        for operation in (mean_mock, median_mock, variance_mock):
            operation.assert_called_once_with(snapshot)
            self.assertIs(operation.call_args.args[0], snapshot)

    def test_validation_failure_prevents_statistics(self):
        module = sys.modules["calc.summary"]
        with patch.object(module, "mean") as mean_mock, \
                patch.object(module, "median") as median_mock, \
                patch.object(module, "variance") as variance_mock:
            with self.assertRaises(CalcError):
                self.summary(iter([1, "x"]))
        for operation in (mean_mock, median_mock, variance_mock):
            operation.assert_not_called()

    def test_calc_error_from_each_statistic_propagates_without_partial_result(self):
        module = sys.modules["calc.summary"]
        for name in ("mean", "median", "variance"):
            with self.subTest(operation=name):
                error = CalcError("statistic failed")
                with patch.object(module, name, side_effect=error):
                    with self.assertRaises(CalcError) as caught:
                        self.summary([1, 2, 3])
                self.assertIs(caught.exception, error)


class SummaryDocumentationTest(unittest.TestCase):
    def test_additional_operations_documents_all_four_exports(self):
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()
        additional = readme.split("## Additional operations\n", 1)[1]
        names = re.findall(r"^- `(mean|median|variance|summary)\(values\)`", additional, re.M)
        self.assertCountEqual(names, ["mean", "median", "variance", "summary"])
        self.assertIn("population", additional)
        self.assertIn("CalcError", additional)
        self.assertEqual(readme.count("are re-exported from the top-level"), 1)
        self.assertNotIn("`power`, `modulo` and `gcd` are re-exported", readme)
        self.assertIn(
            "The operations below are re-exported from the top-level `calc` package. "
            "Each raises `calc.errors.CalcError` on invalid input:",
            " ".join(additional.split()),
        )


if __name__ == "__main__":
    unittest.main()
