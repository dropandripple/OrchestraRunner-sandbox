import subprocess
import sys
import unittest
from pathlib import Path

from calc import gcd, modulo, power


class CalcIntegrationTest(unittest.TestCase):
    def test_geometry_exports_are_the_submodule_functions(self):
        import calc
        from calc import geometry

        for name in ("circle_area", "rectangle_area", "triangle_area", "total_area"):
            with self.subTest(name=name):
                self.assertIs(getattr(calc, name), getattr(geometry, name))

    def test_geometry_operations_via_package(self):
        import math

        from calc import circle_area, rectangle_area, total_area, triangle_area
        from calc.errors import CalcError

        self.assertAlmostEqual(circle_area(2), 4 * math.pi)
        self.assertEqual(rectangle_area(2, 3), 6)
        self.assertEqual(triangle_area(3, 4), 6)
        self.assertAlmostEqual(
            total_area([("circle", (1,)), ("rectangle", (2, 3)), ("triangle", (3, 4))]),
            math.pi + 12,
        )
        self.assertEqual(total_area([]), 0)
        for function, args in (
            (circle_area, (-1,)), (rectangle_area, (0, float("inf"))),
            (triangle_area, (None, 0)), (total_area, (("circle", (1,)),)),
        ):
            with self.subTest(function=function.__name__, args=args):
                with self.assertRaises(CalcError):
                    function(*args)

    def test_power_modulo_gcd_via_package(self):
        # gcd(48, 18) == 6; 6 % 4 == 2; 2 ** 2 == 4
        self.assertEqual(power(modulo(gcd(48, 18), 4), 2), 4)

    def test_statistics_and_summary_via_package(self):
        from calc import mean, median, summary, variance

        values = [3, 1, 2]
        self.assertEqual(mean(values), 2)
        self.assertEqual(median(values), 2)
        self.assertAlmostEqual(variance(values), 2 / 3)
        self.assertEqual(summary(values)["median"], median(values))
        self.assertEqual(
            summary([4, 1, 3, 2]),
            {"mean": 2.5, "median": 2.5, "variance": 1.25},
        )

    def test_package_exports_are_the_submodule_functions(self):
        import calc
        from calc import mean, median, summary, variance
        from calc.summary import summary as module_summary

        for name, function in (
            ("mean", mean), ("median", median), ("variance", variance),
        ):
            with self.subTest(name=name):
                self.assertIs(function, getattr(sys.modules["calc.stats"], name))
                self.assertIs(getattr(calc, name), function)
        self.assertIs(calc.summary, module_summary)
        self.assertIs(summary, sys.modules["calc.summary"].summary)

    def test_invalid_statistics_inputs_via_package(self):
        from calc import mean, median, summary, variance
        from calc.errors import CalcError

        for operation in (mean, median, variance, summary):
            for values in ([], None, [1, "x"], [float("nan")]):
                with self.subTest(operation=operation.__name__, values=values):
                    with self.assertRaises(CalcError):
                        operation(values)

    def test_imports_work_in_a_fresh_interpreter(self):
        for first_import in (
            "from calc.summary import summary",
            "from calc import mean, median, variance, summary",
        ):
            with self.subTest(first_import=first_import):
                result = subprocess.run(
                    [sys.executable, "-c", first_import + "\n"
                     "import calc, sys\n"
                     "assert calc.mean is sys.modules['calc.stats'].mean\n"
                     "assert calc.median is sys.modules['calc.stats'].median\n"
                     "assert calc.variance is sys.modules['calc.stats'].variance\n"
                     "assert calc.summary is sys.modules['calc.summary'].summary\n"
                     "assert summary([4, 1, 3, 2]) == "
                     "{'mean': 2.5, 'median': 2.5, 'variance': 1.25}\n"],
                    cwd=Path(__file__).resolve().parents[1],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
