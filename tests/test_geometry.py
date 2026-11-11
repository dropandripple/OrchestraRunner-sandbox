import ast
import copy
import importlib
import math
import re
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from calc.errors import CalcError


class GeometryTest(unittest.TestCase):
    def setUp(self):
        self.geometry = importlib.import_module("calc.geometry")

    def area_functions(self):
        return (
            (self.geometry.circle_area, 1),
            (self.geometry.rectangle_area, 2),
            (self.geometry.triangle_area, 2),
        )

    def test_formulas_with_integer_float_and_mixed_dimensions(self):
        for name, args, expected in (
            ("circle_area", (2,), 4 * math.pi),
            ("circle_area", (0.5,), math.pi / 4),
            ("rectangle_area", (2, 3), 6),
            ("rectangle_area", (2.5, 1.5), 3.75),
            ("rectangle_area", (2, 1.5), 3),
            ("triangle_area", (3, 4), 6),
            ("triangle_area", (2.5, 1.5), 1.875),
            ("triangle_area", (3, 1.5), 2.25),
        ):
            with self.subTest(function=name, args=args):
                self.assertAlmostEqual(getattr(self.geometry, name)(*args), expected)

    def test_circle_and_triangle_return_floats(self):
        for name, args in (
            ("circle_area", (2,)), ("circle_area", (0,)),
            ("triangle_area", (3, 4)), ("triangle_area", (0, 4)),
        ):
            with self.subTest(function=name, args=args):
                self.assertIsInstance(getattr(self.geometry, name)(*args), float)

    def test_zero_in_each_dimension(self):
        for function, count in self.area_functions():
            for position in range(count):
                for zero in (0, 0.0, -0.0):
                    args = [3] * count
                    args[position] = zero
                    with self.subTest(function=function.__name__, args=args):
                        self.assertEqual(function(*args), 0)

    def test_bools_act_as_zero_and_one_in_each_dimension(self):
        self.assertEqual(self.geometry.circle_area(False), 0)
        self.assertAlmostEqual(self.geometry.circle_area(True), math.pi)
        for function, factor in (
            (self.geometry.rectangle_area, 1),
            (self.geometry.triangle_area, 0.5),
        ):
            for left in (False, True, 3):
                for right in (False, True, 4):
                    with self.subTest(function=function.__name__, args=(left, right)):
                        self.assertEqual(function(left, right), int(left) * int(right) * factor)

    def test_invalid_dimensions_in_every_position_even_beside_zero(self):
        invalid = (
            -1, -0.5, "2", None, float("nan"), float("inf"), float("-inf"),
            1j, Decimal("2"), Fraction(1, 2), [], (), {}, {1}, b"2", object(),
        )
        for function, count in self.area_functions():
            for position in range(count):
                for other in (0, 3):
                    for value in invalid:
                        args = [other] * count
                        args[position] = value
                        with self.subTest(function=function.__name__, args=args):
                            with self.assertRaises(CalcError):
                                function(*args)

    def test_huge_integer_rectangle_products_stay_exact(self):
        huge = 10 ** 400
        for args, expected in (
            ((huge, 2), 2 * huge), ((2, huge), 2 * huge),
            ((huge, huge), huge * huge), ((huge, 0), 0), ((0, huge), 0),
        ):
            with self.subTest(args=args):
                result = self.geometry.rectangle_area(*args)
                self.assertIs(type(result), int)
                self.assertEqual(result, expected)

    def test_float_overflow_and_integer_to_float_overflow_raise_calc_error(self):
        for name, args in (
            ("circle_area", (1e200,)),
            ("circle_area", (10 ** 400,)),
            ("rectangle_area", (1e200, 1e200)),
            ("rectangle_area", (10 ** 400, 2.0)),
            ("triangle_area", (1e200, 1e200)),
            ("triangle_area", (10 ** 400, 2)),
            ("triangle_area", (2, 10 ** 400)),
        ):
            with self.subTest(function=name, args=args):
                with self.assertRaises(CalcError):
                    getattr(self.geometry, name)(*args)

    def test_empty_and_mixed_total_leave_input_unchanged(self):
        self.assertEqual(self.geometry.total_area([]), 0)
        shapes = [("circle", (1,)), ("rectangle", (2, 3)), ("triangle", (3, 4))]
        original = copy.deepcopy(shapes)
        self.assertAlmostEqual(self.geometry.total_area(shapes), math.pi + 12)
        self.assertEqual(shapes, original)
        self.assertAlmostEqual(self.geometry.total_area(shapes), math.pi + 12)

    def test_total_dispatches_each_kind_with_float_bool_and_zero_dimensions(self):
        for kind, args, expected in (
            ("circle", (0.5,), math.pi / 4),
            ("rectangle", (2.5, 1.5), 3.75),
            ("triangle", (2.5, 1.5), 1.875),
            ("circle", (True,), math.pi),
            ("rectangle", (True, 3), 3),
            ("triangle", (3, True), 1.5),
            ("circle", (False,), 0),
            ("rectangle", (2, 0), 0),
            ("triangle", (0, 3), 0),
        ):
            with self.subTest(kind=kind, args=args):
                self.assertAlmostEqual(self.geometry.total_area([(kind, args)]), expected)

    def test_total_rejects_every_non_list_outer_input(self):
        for value in (
            (), (("circle", (1,)),), (entry for entry in [("circle", (1,))]),
            iter([]), None, "", b"", {}, set(), 1, True,
        ):
            with self.subTest(value=value):
                with self.assertRaises(CalcError):
                    self.geometry.total_area(value)

    def test_total_rejects_entries_that_are_not_pairs(self):
        for entry in (None, 1, object(), (), ("circle",), ("circle", (1,), "extra")):
            with self.subTest(entry=entry):
                with self.assertRaises(CalcError):
                    self.geometry.total_area([entry])

    def test_total_rejects_unknown_and_unhashable_kinds(self):
        for kind in ("square", "Circle", "", None, 1, [], {}):
            with self.subTest(kind=kind):
                with self.assertRaises(CalcError):
                    self.geometry.total_area([(kind, (1,))])

    def test_total_rejects_wrong_argument_counts_for_every_kind(self):
        for kind, count in (("circle", 1), ("rectangle", 2), ("triangle", 2)):
            for args in ((), (1,) * (count - 1), (1,) * (count + 1), None, 1):
                with self.subTest(kind=kind, args=args):
                    with self.assertRaises(CalcError):
                        self.geometry.total_area([(kind, args)])

    def test_total_rejects_invalid_dimensions_in_every_position(self):
        for kind, count in (("circle", 1), ("rectangle", 2), ("triangle", 2)):
            for position in range(count):
                for value in (-1, "2", None, float("nan"), float("inf")):
                    args = [0] * count
                    args[position] = value
                    shapes = [("rectangle", (2, 3)), (kind, tuple(args))]
                    with self.subTest(kind=kind, args=args):
                        with self.assertRaises(CalcError):
                            self.geometry.total_area(shapes)

    def test_total_checks_area_and_running_sum_overflow(self):
        for shapes in (
            [("rectangle", (1e200, 1e200))],
            [("circle", (10 ** 400,))],
            [("triangle", (10 ** 400, 2))],
            [("rectangle", (1e308, 1)), ("rectangle", (1e308, 1))],
            [("rectangle", (10 ** 400, 2)), ("circle", (1,))],
        ):
            with self.subTest(shapes=shapes):
                with self.assertRaises(CalcError):
                    self.geometry.total_area(shapes)

    def test_unexpected_errors_from_entry_unpacking_propagate_unchanged(self):
        error = RuntimeError("entry iteration failed")

        class BrokenEntry:
            def __iter__(self):
                raise error

        with self.assertRaises(RuntimeError) as caught:
            self.geometry.total_area([BrokenEntry()])
        self.assertIs(caught.exception, error)

    def test_unexpected_errors_from_argument_length_propagate_unchanged(self):
        error = RuntimeError("argument length failed")

        class BrokenArgs:
            def __len__(self):
                raise error

        with self.assertRaises(RuntimeError) as caught:
            self.geometry.total_area([("circle", BrokenArgs())])
        self.assertIs(caught.exception, error)

    def test_calc_error_from_area_function_propagates_unchanged(self):
        error = CalcError("area calculation failed")

        class BrokenDimension(int):
            def __mul__(self, other):
                raise error

            def __rmul__(self, other):
                raise error

        with self.assertRaises(CalcError) as caught:
            self.geometry.total_area([("rectangle", (BrokenDimension(2), 3))])
        self.assertIs(caught.exception, error)


class GeometryDocumentationTest(unittest.TestCase):
    def setUp(self):
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text()
        self.additional = readme.split("## Additional operations\n", 1)[1].split("\n## ", 1)[0]

    def test_additional_operations_has_a_bullet_for_each_geometry_export(self):
        for signature in (
            "circle_area(r)", "rectangle_area(w, h)",
            "triangle_area(base, height)", "total_area(shapes)",
        ):
            with self.subTest(signature=signature):
                self.assertRegex(self.additional, r"(?m)^- `" + re.escape(signature) + r"`")

    def test_total_documents_kinds_argument_counts_and_empty_list_result(self):
        text = " ".join(self.additional.replace("`", "").split())
        for kind, count in (("circle", "1|one"), ("rectangle", "2|two"), ("triangle", "2|two")):
            with self.subTest(kind=kind):
                self.assertRegex(text, rf"\b{kind}\b[^.;]*\b({count})\s+(?:args?|arguments?|dimensions?)\b")
        self.assertRegex(text, r"total_area\(\[\]\)\s+(?:returns|gives|is|==|=)\s+0\b")

    def test_readme_has_a_mixed_total_area_example(self):
        examples = re.findall(r"total_area\(\s*\[.*?\]\s*\)", self.additional, re.S)
        kinds_in_examples = []
        for example in examples:
            try:
                call = ast.parse(example, mode="eval").body
                shapes = ast.literal_eval(call.args[0])
            except (SyntaxError, ValueError, TypeError):
                continue
            if shapes and all(isinstance(shape, (list, tuple)) and len(shape) == 2 for shape in shapes):
                kinds_in_examples.append({shape[0] for shape in shapes})
        self.assertIn({"circle", "rectangle", "triangle"}, kinds_in_examples)

    def test_geometry_input_rules_have_a_sentence_separate_from_statistics(self):
        sentences = re.split(r"(?<=[.!?])\s+", " ".join(self.additional.split()))
        statistics_rules = [s for s in sentences if "These input rules apply to all four statistics" in s]
        self.assertEqual(len(statistics_rules), 1)
        geometry_rules = [
            s for s in sentences
            if re.search(r"\b(?:dimensions?|geometry)\b", s, re.I)
            and re.search(r"\bint(?:eger)?s?\b", s)
            and re.search(r"\bfloats?\b", s)
        ]
        self.assertTrue(geometry_rules, "Document geometry dimension types in their own sentence")
        for sentence in geometry_rules:
            self.assertNotIn("all four statistics", sentence)


if __name__ == "__main__":
    unittest.main()
