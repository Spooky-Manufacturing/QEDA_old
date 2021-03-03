import unittest
from math import pi
from random import randint
# from context import GateMaker


class GateMakerTest(unittest.TestCase):
    def setUp(self):
        self.gm = GateMaker
        pass

    def test_test(self):
        pass

    def test_idle_gate(self):
        i = self.gm.u3(0, 0, 0)
        self.assertEqual(i.simulate(0, 0, 0), (0, 0, 0))

    def test_pauli_x(self):
        x = self.gm.u3(pi, 0, pi)
        self.assertEqual(x.simulate(0, 0, 0), (1, 0, 1))

    def test_pauli_y(self):
        y = self.gm.u3(pi, pi/2, pi/2)
        self.assertEqual(y.simulate(0, 0, 0), (1, 0.5, 0.5))

    def test_pauli_z(self):
        z = self.gm.u1(pi)
        self.assertEqual(z.simulate(0, 0, 0), (0, 0, 1))

    def test_hadamard(self):
        h = self.gm.u2(0, pi)
        self.assertEqual(h.simulate(0, 0, 0), (0, 0.5, 0.5))

    def test_clifford_gate(self):
        s = self.gm.u1(pi/2)
        self.assertEqual(s.simulate(0, 0, 0), (0, 0, .5))

    def test_clifford_conjugate(self):
        sdg = self.gm.u1(-pi/2)
        self.assertEqual(sdg.simulate(0, 0, 0), (0, 0, -.5))

    def test_c3_gate(self):
        t = self.gm.u1(pi/4)
        self.assertEqual(t.simulate(0, 0, 0), (0, 0, 0.25))

    def test_c3_conjugate(self):
        tdg = self.gm.u1(pi/4)
        self.assertEqual(tdg.simulate(0, 0, 0), (0, 0, -0.25))

    def test_x_rotation(self):
        theta = randint(0, 180)
        rx = self.gm.u3(theta, -pi/2, pi/2)
        self.assertEqual(rx.simulate(0, 0, 0), (theta, -pi/2, pi/2))

    def test_y_rotation(self):
        theta = randint(0, 180)
        ry = self.gm.u3(theta, 0, 0)
        self.assertEqual(rx.simulate(0, 0, 0), (theta, 0, 0))

    def test_z_rotation(self):
        phi = randint(0, 180)
        rz = self.gm.u1(phi)
        self.assertEqual(rz.simulate(0, 0, 0), (0, 0, phi))

    def test_controlled_not(self):
        cx = self.gm.CX()
        self.assertEqual(cx.simulate([[0, 0, 0], [0, 0, 0]]), ([[0, 0, 0], [1, 1, 1]]))

    def test_controlled_phase(self):
        # set qubit start
        a = [0, 0, 1]
        b = [1, 1, 1]
        # define gates
        h = self.gm.u2(0, pi)
        cx = self.gm.CX()
        # Simulate cphase
        b = h.simulate(b)
        a, b = cx.simulate(a, b)
        b = h.simulate(b)
        # Check results
        self.assertEqual(a, [0, 0, 0])
        self.assertEqual(b, [1, 1, 0])

    def test_controlled_y(self):
        # set qubit start
        a = [0, 1, 0]
        b = [0, 0, 0]
        # define gates
        s = self.gm.u1(pi/2)
        sdg = self.gm.u1(-pi/2)
        cx = self.gm.CX()
        # Simulate cphase
        b = sdg.simulate(b)
        a, b = cx.simulate(a, b)
        b = s.simulate(b)
        # Check results
        self.assertEqual(a, [0, 1, 0])
        self.assertEqual(b, [1, 0, 1])

    def test_controlled_h(self):
        # set qubit start
        control = [0, 0, 0]
        target = [1, 1, 1]
        h = self.gm.u2(0, pi)
        sdg = self.gm.u1(-pi/2)
        cx = self.gm.CX()
        t = self.gm.u1(pi/4)
        s = self.gm.u1(pi/2)

        b = h.simulate(b)
        b = sdg.simulate(b)
        a, b = cx.simulate(a, b)
        b = t.simulate(b)
        b = h.simulate(b)

    def test_measure(self):
        pass

    def test_cx(self):
        pass

    def test_arbitrary_u(self):
        pass

    def test_ccx(self):
        pass


if __name__ == '__main__':
    unittest.main()
