#!/usr/bin/python3
#from pykicad.pcb import *
#from pykicad.module import *
# Import globals
from qeda.qast_primitives import CONFIG, SEL, LIB, QCODE

config = CONFIG
# Import gate primitives
from qeda.qast_primitives import End, Int, Char, Real, String, BinaryOp, Component, UQGate, CQGate, CustomQGate


class OpenQASM():
    def __init__(self, value):
        self.version = value

    def eval(self):
        return self.version


class GateDecl():
    def __init__(self, gate_name, args=None, controls=None, targets=None):
        self.name = gate_name
        self.args = None
        self.footprint = None
        if controls:
            self._add_controls(controls)
        if targets:
            self._add_targets(targets)

    def _add_controls(self, controls):
        self.controls = [x.value for x in controls]

    def _add_targets(self, targets):
        self.targets = [x.value for x in targets]

    def gate_definition(self):
        pass


class CREG(Component):
    """The classical register.
    n: Integer representing the number of bits to store
    """
    def __init__(self, n):
        self.qid = -1
        self._add_register(n, 'CREG')


class QREG(Component):
    """The quantum register.
    n: Integer representing the number of qubits to store.
    """
    def __init__(self, n):
        self.n = n
        self.qid = range(1, len(n))
        self._set_footprint('QREG')


class H(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('HGate')


class I(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('IGate')


class S(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('SGate')


class SDG(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('SDGGate')


class T(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('TGate')


class TDG(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('TDGGate')


class X(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('XGate')


class Y(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('YGate')


class Z(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('ZGate')


class RX(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('RXGate')


class RY(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('RYGate')


class RZ(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('RZGate')


class Measure(UQGate):
    def __init__(self, qid):
        UQGate.__init__(self, qid)
        self._set_footprint('Measure')


class CX(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CXGate')


class CYGate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CYGate')


class CZGate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CZGate')


class CHGate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CHGate')


class CCXGate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CCXGate')


class CRZGate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CRZGate')


class CU1Gate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CU1Gate')


class CU3Gate(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CU3Gate')
