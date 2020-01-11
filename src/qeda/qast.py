from numpy import array
#from pykicad.pcb import *
#from pykicad.module import *
import configparser
# Setup the configurations
config = configparser.ConfigParser()
config.read('lib/components.conf')
# Grab Global Configs
SEL = config['PROJECT']['SELECTION'] # Currently selected configs
CSIZE = config[SEL]['OpticSize'] # Component size
MOUNT = config[SEL]['Mounting'] # Mounting Configuration
LIB = config[SEL]['QLib'] # Component Library

# QCode Dict
qcode = {
    }

class End():
    def eval(self):
       return 0

class OpenQASM():
    def __init__(self, value):
        self.version = value

    def eval(self):
        return self.version

class Int():
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

    def _add_register(self, n, t):
        """n: Int; number of bits/qubits
           t: string; type of register"""
        pass
    def _set_footprint(self, fp):
        #self.footprint = Module.from_library(LIB, config[CSIZE][fp]) # Final code
        self.footprint = [LIB, config[CSIZE][fp]] # Testing Code
        self._add_qcomponent(self.qid)

    def _add_qcomponent(self, qid):
        """Adds the components to master dictionary"""
        try:
            # If the qid is of type Number we need to convert to integer
            if type(qid) != type(1):
                qid = qid.eval()
            # If component is applied to all qubits
            if qid == -1:
                for key, value in qcode.items():
                    qcode[key].append(self.footprint)
            # If component is a CREG or QREG
            elif qid == -2:
                for key, value in qcode.items():
                    qcode[key].append(self.footprint)
                pass
            # If the qubit isn't already listed, add new qubit
            # qcode = { 0: [], 1: [],...}
            elif qid not in qcode:
                # create a list and append instruction
                qcode[qid] = [self.footprint]
            else:
                # append instuctions to existing qubit
                qcode[qid].append(self.footprint)
        except Exception as e:
            print("exception", e)
            pass
    def eval(self):
        return self.footprint, qcode

class UQGate(Component):
    """The Unitary Quantum Gates.
    qid: Integer representing the qubit (starting from 0 to +N)
    footprint: pykicad module object
    """
    def __init__(self, qid):
        self.qid = qid
        self.footprint = None

    def eval(self):
        return self.footprint
    pass

class CQGate(Component):
    """Controlled Quantum Gates
    control: Control qubit
    targets: list of qubits that are controlled by CQGate
    """
    def __init__(self, control, targets):
        self.qid = control
        self.targets = targets
        self.footprint = None

    def eval(self):
        return self.qid, self.targets, self.footprint

class CustomQGate(Component):
    """Class for custom Quantum Gates"""
    def __init__(self, gate_name, control=None, targets=None):
        self.name = gate_name
        self.qid = control
        self.targets = targets
        self.footprint = None

    def _set_footprint(self, lib, fp):
        self.footprint = Module.from_library(lib, fp)

    def eval(self):
        return self.qid, self.targets, self.footprint

class GateDecl():
    def __init__(self, gate_name, args=None, controls=None, targets=None):
        self.name = gate_name
        self.args = None
        self.footprint = None
        self._add_controls(controls)
        self._add_targets(targets)

    def _add_controls(self, controls):
        self.controls = [x.value for x in controls]

    def _add_targets(self, targets):
        self.targets = [x.value for x in targets]

class CREG(Component):
    """The classical register.
    n: Integer representing the number of bits to store
    """
    def __init__(self, n):
        self.qid = -1
        self._add_register(n,'CREG')

class QREG(Component):
    """The quantum register.
    n: Integer representing the number of qubits to store.
    """
    def __init__(self, n):
        self.n = n
        self.qid = range(1,len(n))
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

class Measure(UQGate):
    def __init__(self, qid):
        self.qid = qid
        self._set_footprint('MEASURE')
