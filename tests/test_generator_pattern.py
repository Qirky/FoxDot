import unittest

from FoxDot.lib.Patterns import GeneratorPattern
from FoxDot.lib.Patterns import P

class TestPatternMethods(unittest.TestCase):
    def test_from_func(self):
        def some_generation_func(index):
            if index == 3:
                return 2
            else:
                return 1
        pattern = GeneratorPattern.from_func(some_generation_func)
        self.assertTrue(isinstance(pattern, GeneratorPattern))
        self.assertEqual(pattern[:4], P[1, 1, 1, 2])


if __name__ == "__main__":

    unittest.main()
