import unittest
from tests.context import qast

class QAST_Tests(unittest.TestCase):
    def setUp(self):
        self.end = qast.End
        self.open_qasm = qast.OpenQASM
        self.int = qast.Int
        self.char = qast.Char
        self.binop = qast.BinaryOp
        self.component = qast.Component
        self.uq_gate = qast.UQGate
        self.cq_gate = qast.CQGate
        self.custom_q_gate = qast.CustomQGate
        self.h = qast.H
        self.i = qast.I
        self.s = qast.S
        self.sdg = qast.SDG
        self.t = qast.T
        self.tdg = qast.TDG
        self.x = qast.X
        self.y = qast.Y
        self.z = qast.Z
        self.rx = qast.RX
        self.ry = qast.RY
        self.rz = qast.RZ
        self.cx = qast.CX
        self.cy = qast.CYGate
        self.cz = qast.CZGate
        self.ch = qast.CHGate
        self.ccx = qast.CCXGate
        self.crz = qast.CRZGate
        self.cu1 = qast.CU1Gate
        self.cu3 = qast.CU3Gate
        self.measure = qast.Measure

    def test_end(self):
        self.assertEqual(self.end().eval(), (qast.QCODE, 0))

    def test_openq(self):
        self.assertEqual(self.open_qasm(1).eval(), 1)

    def test_integer(self):
        self.assertEqual(self.int(10).eval(), 10)

    def test_char(self):
        self.assertEqual(self.char('X').eval(), 'X')

    def test_binop(self):
        pass

    def test_component(self):
        self.assertEqual(self.component().eval(), None)

    def test_uq_gate(self):
        self.assertEqual(self.uq_gate(1).eval(), None)

    def test_cq_gate(self):
        control = 1
        targets = [2,3,4,5]
        self.assertEqual(self.cq_gate(control=control, targets=targets).eval(),
                         (control, targets, None))

    def test_custom_q_gate(self):
        self.assertEqual(self.custom_q_gate('test').eval(),
                         (None, None, None))
        control = 1
        targets = [2,3,4]
        self.assertEqual(self.custom_q_gate('test', control, targets).eval(),
                         (control, targets, None))

    def test_h_gate(self):
        self.assertEqual(self.h(0).eval(),
                         (qast.LIB, 'HGate'))

    def test_i_gate(self):
        self.assertEqual(self.i(0).eval(),
                         (qast.LIB, 'IGate'))

    def test_s_gate(self):
        self.assertEqual(self.s(0).eval(),
                         (qast.LIB, 'SGate'))

    def test_sdg_gate(self):
        self.assertEqual(self.sdg(0).eval(),
                         (qast.LIB, 'SDGGate'))

    def test_t_gate(self):
        self.assertEqual(self.t(0).eval(),
                         (qast.LIB, 'TGate'))

    def test_tdg_gate(self):
        self.assertEqual(self.tdg(0).eval(),
                         (qast.LIB, 'TDGGate'))

    def test_x_gate(self):
        self.assertEqual(self.x(0).eval(),
                         (qast.LIB, 'XGate'))

    def test_y_gate(self):
        self.assertEqual(self.y(0).eval(),
                         (qast.LIB, 'YGate'))

    def test_z_gate(self):
        self.assertEqual(self.z(0).eval(),
                         (qast.LIB, 'ZGate'))


    def test_rx_gate(self):
        self.assertEqual(self.rx(0).eval(),
                         (qast.LIB, 'RXGate'))


    def test_rz_gate(self):
        self.assertEqual(self.rz(0).eval(),
                         (qast.LIB, 'RZGate'))

    def test_cx_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.cx(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CXGate')))

    def test_cy_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.cy(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CYGate')))

    def test_cz_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.cz(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CZGate')))

    def test_ch_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.ch(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CHGate')))

    def test_ccx_gate(self):
        control = 1
        targets = [2,3]
        self.assertEqual(self.ccx(control, targets).eval(),
                         (control, targets,
                          (qast.LIB, 'CCXGate')))

    def test_crz_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.crz(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CRZGate')))

    def test_cu1_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.cu1(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CU1Gate')))

    def test_cu3_gate(self):
        control = 1
        target = 2
        self.assertEqual(self.cu3(control, target).eval(),
                         (control, target,
                          (qast.LIB, 'CU3Gate')))

    def test_measurement(self):
        self.assertEqual(self.measure(0).eval(),
                         (qast.LIB, 'MEASURE'))
if __name__ == '__main__':
    unittest.main()
