from primitives import U1, U2, U3

class X(U3):
    def __init__(self):
        self.theta = pi
        self.phi = 0
        self.lamda = pi
        pass

class Y(U3):
    def __init__(self):
        self.theta = pi
        self.phi = pi/2
        self.lamda = pi/2
        pass

class Z(U1):
    def __init__(self):
        self.lamda = pi
        pass

class H(U2):
    def __init__(self):
        self.phi = 0
        self.lamda = pi

class S(U1):
    def __init__(self):
        self.lamda = pi/2

class SDG(U1):
    def __init__(self):
        self.lamda = -pi/2

class T(U1):
    def __init__(self):
        self.lamda = pi/4

class TDG(U1):
    def __init__(self):
        self.lamda = -pi/4

class RX(U3):
    def __init__(self, theta):
        self.theta = theta
        self.phi = -pi/2
        self.lamda = pi/2

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
