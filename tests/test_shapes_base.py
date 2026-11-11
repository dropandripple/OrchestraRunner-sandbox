import unittest
from pathlib import Path


class ShapesBaseTest(unittest.TestCase):
    def test_package_files_exist(self):
        package_dir = Path(__file__).resolve().parents[1] / "shapes"

        for filename in ("__init__.py", "base.py"):
            with self.subTest(filename=filename):
                self.assertTrue((package_dir / filename).is_file())

    def test_version_is_two(self):
        from shapes.base import VERSION

        self.assertIs(type(VERSION), int)
        self.assertEqual(VERSION, 2)


if __name__ == "__main__":
    unittest.main()
