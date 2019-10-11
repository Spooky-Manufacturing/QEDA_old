from numpy import array
from pykicad.pcb import *
from pykicad.module import *
import configparser
# Setup the configurations
config = configparser.ConfigParser()
config.read('lib/components.conf')
# Grab Global Configs
SEL = config['PROJECT']['SELECTION'] # Currently selected configs
CSIZE = config[SEL]['OpticSize'] # Component size
MOUNT = config[SEL]['Mounting'] # Mounting Configuration
LIB = config[SEL]['QLib'] # Component Library

# QCode List
qcode = [[],[],[]]

class End():
    def eval(self):
        return 0
        
class OpenQASM():
    def __init__(self, value):
        self.version = value

    def eval(self):
        return self.version

class Number():
    def __init__(self, value):
        self.value=value

    def eval(self):
        return int(self.value)

class Char():
    def __init__(self, value):
        self.value = value
        
    def eval(self):
        return self.value

class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Component():
    """The Component primitive"""
    def __init__(self):
        global qcode
        global SEL
        global CSIZE
        global MOUNT
        global LIB
        self.footprint = None
        self.qid = None


    def _set_footprint(self, fp):
        #self.footprint = Module.from_library(LIB, config[CSIZE][fp]) # Final code
        self.footprint = (LIB, config[CSIZE][fp]) # Testing Code
        self._add_qcomponent(self.qid)

    def _add_qcomponent(self, qid):
        """Adds the components to master list"""
        qcode[int(qid.eval())].append(self.footprint)
        print(qcode)

class UQGate(Component):
    """The Unitary Quantum Gates.
    qid: Integer representing the qubit (starting from 0 to +N)
    footprint: pykicad module object
    """
    def __init__(self, qid):
        self.qid = qid
        self.footprint = None
        
    def eval(self):
        # Add gate to
#        return self.qid, self.footprint
# testing
        return self.footprint
    pass

class CQGate(Component):
    """Controlled Quantum Gates
    control: Control qubit
    targets: list of qubits that are controlled by CQGate
    """
    def __init__(self, control, targets):
        self.control = control
        self.targets = targets
        self.footprint = None

    def eval(self):
        return self.control, self.targets, self.footprint

class CustomQGate(Component):
    """Class for custom Quantum Gates"""
    def __init__(self, qid=None, control=None, targets=None):
        self.qid = qid
        self.control = control
        self.targets = targets

    def _set_footprint(self, lib, fp):
        self.footprint = Module.from_library(lib, fp)

    def eval(self):
        return self.qid, self.control, self.targets, self.footprint
        
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
        self._set_footprint('SGATE')

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

class CX(CQGate):
    def __init__(self, control, targets):
        CQGate.__init__(self, control, targets)
        self._set_footprint('CQGate')
            
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

class Measure():
    def __init__(self):
        self.footprint = Module.from_library
