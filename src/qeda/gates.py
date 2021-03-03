from primitives import U1, U2, U3


PI = 3.14159


class X(U3):
    def __init__(self):
        self.theta = PI
        self.phi = 0
        self.lamda = PI


class Y(U3):
    def __init__(self):
        self.theta = PI
        self.phi = PI / 2
        self.lamda = PI / 2


class Z(U1):
    def __init__(self):
        self.lamda = PI


class H(U2):
    def __init__(self):
        self.phi = 0
        self.lamda = PI


class S(U1):
    def __init__(self):
        self.lamda = PI / 2


class SDG(U1):
    def __init__(self):
        self.lamda = -PI / 2


class T(U1):
    def __init__(self):
        self.lamda = PI / 4


class TDG(U1):
    def __init__(self):
        self.lamda = -PI / 4


class RX(U3):
    def __init__(self, theta):
        self.theta = theta
        self.phi = -PI / 2
        self.lamda = PI / 2


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
