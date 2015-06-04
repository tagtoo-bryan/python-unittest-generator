import unittest
import math

class Testmath(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_copysign(self):
        self.assertEqual(math.copysign(1.2, -2.3), -1.2)
        return

    def test_ceil(self):
        self.assertEqual(math.ceil(1.2), 2.0)
        self.assertEqual(math.ceil(-1.2), -1.0)
        return




if __name__ == '__main__':
    unittest.main()