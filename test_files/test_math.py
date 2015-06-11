import unittest
import math

class Testmath(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_copysign(self):

        result = math.copysign(1.2, -2.3)

        self.assertEqual(result, -1.2)

        return

    def test_ceil(self):

        result = math.ceil(1.2)

        self.assertEqual(result, 2.0)


        self.assertRaises(TypeError, math.ceil,"5")


        return




if __name__ == '__main__':
    unittest.main()
