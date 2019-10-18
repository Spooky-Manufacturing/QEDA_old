from primitives import U1, U2, U3

global PI
PI = 3.14159

class X(U3):
    global PI
    def __init__(self):
        self.theta = PI
        self.phi = 0
        self.lamda = PI
        pass

class Y(U3):
    global PI
    def __init__(self):
        self.theta = PI
        self.phi = PI/2
        self.lamda = PI/2
        pass

class Z(U1):
    global PI
    def __init__(self):
        self.lamda = PI
        pass

class H(U2):
    global PI
    def __init__(self):
        self.phi = 0
        self.lamda = PI

class S(U1):
    global PI
    def __init__(self):
        self.lamda = PI/2

class SDG(U1):
    global PI
    def __init__(self):
        self.lamda = -PI/2

class T(U1):
    global PI
    def __init__(self):
        self.lamda = PI/4

class TDG(U1):
    global PI
    def __init__(self):
        self.lamda = -PI/4

class RX(U3):
    global PI
    def __init__(self, theta):
        self.theta = theta
        self.phi = -PI/2
        self.lamda = PI/2

class RY(U3):
    def __init__(self, theta):
        self.theta = theta
        self.phi = 0
        self.lamda = 0

class RZ(U1):
    def __init__(self, lamda):
        self.lamda = lamda


class NS():
    """The Non-Linear Sign-Shift Gate.

    Gives a nonlinear phse shift on one mode conditioned on two ancilla modes"""

    def __init__(self):
        pass
