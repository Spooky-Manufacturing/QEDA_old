import unittest
from gate_designer import Bloch


class TestBlochSphere(unittest.TestCase):

    def setUp(self):
        self.bloch = Bloch()
        
    def test_init(self):
        self.assertEqual(self.bloch.x, 0)
        self.assertEqual(self.bloch.y, 0)
        self.assertEqual(self.bloch.z, 0)

    def test_xshift(self):
        self.bloch._xshift(1)
        self.assertEqual(self.bloch.x, 1)

    def test_yshift(self):
        self.bloch._yshift(1)
        self.assertEqual(self.bloch.y, 1)

    def test_zshift(self):
        self.bloch._zshift(1)
        self.assertEqual(self.bloch.z, 1)

    def test_ret_vals(self):
        self.assertEqual(self.bloch.ret_vals(), [0,0,0])

class TestU1Transforms():
    pass

if __name__ == '__main__':
    unittest.main()
