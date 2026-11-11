import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


class ShapesTotalTest(unittest.TestCase):
    def test_total_module_file_exists(self):
        total_path = Path(__file__).resolve().parents[1] / "shapes" / "total.py"

        self.assertTrue(total_path.is_file())

    def test_total_is_nine(self):
        from shapes.total import total

        self.assertEqual(total(), 9)

    def test_total_uses_imported_left_and_right(self):
        from shapes import left, right

        total_path = Path(__file__).resolve().parents[1] / "shapes" / "total.py"

        for left_value, right_value in ((3, 10), (8, 6), (0, 0), (-4, 11), (5, -12)):
            with self.subTest(left=left_value, right=right_value):
                with patch.object(left, "LEFT", left_value), patch.object(
                    right, "RIGHT", right_value
                ):
                    spec = importlib.util.spec_from_file_location(
                        "shapes.total", total_path
                    )
                    total_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(total_module)

                    self.assertEqual(total_module.total(), left_value + right_value)


if __name__ == "__main__":
    unittest.main()
