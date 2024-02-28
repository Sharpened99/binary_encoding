import unittest

from helpers import *
import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(count_tokens(127), 7)  # add assertion here

        self.assertEqual(get_overlap(7, 8), 0)
        self.assertEqual(get_overlap(127, 7), 3)

        main.BITS = 7
        main.FILTER_SIZE = 54
        self.assertEqual(main.maximum_all_perm_tokens(), 4)


if __name__ == '__main__':
    unittest.main()
