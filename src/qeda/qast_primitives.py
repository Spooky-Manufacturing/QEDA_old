import configparser


CONFIG = configparser.ConfigParser()
CONFIG.read('conf/components.conf')
SEL = CONFIG['PROJECT']['SELECTION']  # Current Configs
LIB = CONFIG[SEL]['QLib']  # Component Library

QCODE = {}


class End():
    def __init__(self):
        global QCODE

    def eval(self):
        return QCODE, 0


class Int():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Real():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)


class Char():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class String():
    def __init__(self, string):
        self.string = string

    def eval(self):
        return self.string


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Component:
    """The Component Primitive

    qid: Integer representing the qubit
    footprint: Pykicad module object
    """
    def __init__(self):
        global QCODE
        global SEL
        global LIB
        self.footprint = None
        self.qid = None

    def _set_footprint(self, fp):
        #self.footprint = Module.from_library(LIB, fp)  # Final code
        self.footprint = (LIB, fp)  # Testing code
        self._add_qcomponent(self.qid)

    def _add_qcomponent(self, qid):
        """Adds the components to master dictionary"""
        try:
            # If the qid is of type Number we need to convert to integer
            if type(qid) != type(1):
                qid = qid.eval()
            # If component is applied to all qubits
            if qid == -1:
                for key, value in QCODE.items():
                    QCODE[key].append(self.footprint)
            # If component is a CREG or QREG
            elif qid == -2:
                for key, value in QCODE.items():
                    QCODE[key].append(self.footprint)
                pass
            # If the qubit isn't already listed, add new qubit
            # qcode = { 0: [], 1: [],...}
            elif qid not in QCODE:
                # create a list and append instruction
                QCODE[qid] = [self.footprint]
            else:
                # append instuctions to existing qubit
                QCODE[qid].append(self.footprint)
        except Exception as e:
            print("exception", e)
            pass

    def eval(self):
        return self.footprint, QCODE


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


class CQGate(Component):
    """The Controlled Quantum Gates.
    contol: Control qubit
    targets: lit of qubits that are controlled by CQGate"""
    def __init__(self, control, targets=None):
        global QCODE
        self.qid = control
        self.targets = targets
        self.footprint = ''

    def _set_target(self, target, indicator):
        if target not in QCODE:
            QCODE[target] = [indicator]
        else:
            QCODE[target].append(indicator)

    def set_targets(self):
        indicator = self.footprint + 'TGT'
        if 'Int' in str(type(self.targets)):
            self.targets.eval()
            self._set_target(self.targets, indicator)
        else:
            for target in self.targets:
                if type(target) != type(int):
                    target.eval()
                self._set_target(target, indicator)
#    def eval(self):
#        return self.qid, self.targets, self.footprint


class CustomQGate(Component):
    """Class for Custom Quantum Gates."""
    def __init__(self, gate_name, control=None, targets=None):
        self.name = gate_name
        self.qid = control
        self.targets = targets
        self.footprint = None

    def eval(self):
        print(self.qid)
        return self.qid, self.targets, self.footprint
