import unittest
import math

class Testmath(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_ceil(self):
        self.assertEqual(math.ceil(1.2), 2.0)
        return



if __name__ == '__main__':
    unittest.main()