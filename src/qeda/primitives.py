from math import pi, sin, cos


class Rotation():
    """Specifies the rotation matrix applied to the blochsphere"""
    def __init__(self):
        pass

    def _deg_to_rad(self, deg):
        """Converts degrees to radians"""
        rpd = pi / 180  # Radians per degree
        return deg * rpd

    def _rad_to_deg(self, rad):
        """Converts radians to degrees"""
        rpd = pi / 180
        return rad / rpd

    def isDeg(self, n):
        """Determines if value n is an angle"""
        if type(n) == type(1):
            if n in range(-360, 360):
                return True
            else:
                return False

    def rotate(self, axis, angle):
        """Applies rotation of angle along axis
        axis = axis of rotation
        angle = degree/radian of angle to be rotated by
        """
        if type(self._rad_to_deg(angle)) == type(int(0)):
            # Use radians
            pass
        else:
            # use degrees
            pass


class Mirror(Rotation):
    def __init__(self, angle=45):
        self.angle = angle  # Angle of incidence in degrees, default 45
        pass

    def set_angle(self, n):
        """Sets the angle to n"""
        if not self.isDeg(n):
            self.angle == self._rad_to_deg(n)
        else:
            self.angle == n

    def simple_rotation(self, axis):
        """Performs a simple rotation along a single axis"""
        if self.isDeg(axis):
            return self.angle + axis
        else:
            return self.angle + self._rad_to_deg(axis)
        pass

    def full_rotation(self, m):
        """Performs a full rotation along all axis
        m[x, y]

        x = angle
        y = angle
        """
        if not self.isDeg(m[0]):
            x = self._rad_to_deg(m[0])
        if not self.isDeg(m[1]):
            y = self._rad_to_deg(m[1])

        h = x * cos(self.angle) - y * sin(self.angle)
        v = x * sin(self.angle) + y * cos(self.angle)
        return h, v

#        cos(theta), -sin(theta)
#        sin(theta), cos(theta)


class BeamSplitter(Mirror):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0

    def simulate(self):
        """Simulates the rotations"""
        self.simple_rotation(self.x)
        pass

    def build(self):
        """Builds the component"""
        pass


class PhaseShift():
    def __init__(self, n1=1.00029, n2=1.5, t=500, lamda=650):
        """Phase shifting material.

        Defaults are air at STP and average RI of standard optical glass.
        n1 = first refractive index, default: AIR
        n2 = second refractive index, default: GLASS
        t = thickness in nm, default 500
        lamda = light wavelength, default 650nm"""
        self.n1 = n1
        self.n2 = n2
        self.t = t
        self.lamda = lamda

    def _t_calc(self, phase, accuracy):
        # first we need to get within integer range
        while True:
            x = int(self._phase_shift())
            iphase = int(phase)
            # Just incase any incredibly large numbers are found
            if x > iphase:
                if x > iphase % 2:
                    self.t = self.t / 2
                else:
                    self.t -= 1
            elif x < iphase:
                if x < iphase % 2:
                    self.t = self.t * 2
                else:
                    self.t += 1
            else:
                break
        while True:
            x = self._phase_shift()
            if round(x, accuracy) > round(phase, accuracy):
                self.t -= float(''.join(['1' if i is max(range(accuracy))
                                         else '0.0' if i is min(range(accuracy))
                                         else '0' for i in range(accuracy)]))
            elif round(x, accuracy) < round(phase, accuracy):
                self.t = self.t + float(''.join(['1' if i is max(range(accuracy))
                                         else '0.0' if i is min(range(accuracy))
                                         else '0' for i in range(accuracy)]))
            else:
                break

    def t_calc(self, phase, accuracy=3):
        """Calculates the thickness of material needed to create a given
        phase shift"""
        self._t_calc(phase, accuracy)
        return round(self.t, accuracy)

    def _phase_shift(self):
        return (2 * pi * (self.n2 - self.n1) * self.t) / self.lamda


class Polarizer():
    """polarization calculations"""

    def __init__(self, start, rotation, axis):
        self.start = start
        self.rotation = rotation
        self.axis = axis

    def eval(self):
        pass


class Bloch():
    """Represents the bloch sphere of a photon to be used for simulation and
        testing purposes
    theta, phi, lamda
    z, y, z"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def _xshift(self, x):
        self.x += x

    def _yshift(self, y):
        self.y += y

    def _zshift(self, z):
        self.z += z

    def ret_vals(self):
        return [self.x, self.y, self.z]

    def rotation(self, axis, angle):
        pass
    pass


class U():
    """Defines a basic quantum gate"""
    def __init__(self, theta, phi, lamda):
        self.theta = theta
        self.phi = phi
        self.lamda = lamda
        self.components = None
        pass

    def _build_gate(self):
        """Performs computations necessary to design a physical optical gate"""
        pass

    def _eval_z(self):
        """Evaluates the Z shift"""
        z = PhaseShift()
        t = z.t_calc(self.lamda)
        return t

    def _eval_x(self):
        """Evaluates the X rotation"""
        pass

    def _eval_y(self):
        """Evaluates the Y rotation"""
        pass

    def eval(self):
        """Evaluates all rotations and shifts performed through the gate"""
        pass

    def build(self):
        """Builds the gate as a PCB component"""
        pass

    def _rotate(self, axis, angle):
        pass

    """
    U(theta, phi, lamda) := U(pi/2, pheta, lamda :=
    Rz(phi + 3pi), Rx(pi/2), Rz(theta + pi), Rx(pi/2), Rz(lamda)
    """


class U1(U):
    """Performs lamda transformations
        Equivalent to a Z transformation changing the PHASE of the qubit
        without changing anything else.
    """
    def __init__(self, lamda):
        super().__init__(0, 0, lamda)
        pass

    def eval(self):
        """Used to simulate the gate logic"""
        z = PhaseShift()
        t = z.t_calc(self.lamda)
        return t


class U2(U):
    """Performs phi  and lamda transformations
        Equivalent to an X, Z, transformation changing the PHASE of the quit and
        applying an x rotation.
    """
    def __init(self, phi, lamda):
        super().__init__(pi / 2, phi, lamda)
        pass


class U3(U):
    """Performs theta , phi, and lambda transformations
    Changes phase, x and y rotations.
    """
    def __init__(self, theta, phi, lamda):
        super().__init__(theta, phi, lamda)
        pass


class CX():
    """Controlled X Gate"""
    def __init__(self):
        pass


class CU1():
    """Controlled phase rotation"""
    def __init__(self, lamda):
        '''
        U(0,0,theta/2) a;
        CX a,b;
        U(0,0,-theta/2) b;
        CX a,b;
        U(0,0, theta/2) b
        '''
    pass


class CU3():
    """Controlled-U(theta, phi, lambda) with target t and control c"""
    def __init__(self, theta, phi, lamda, t, c):
        '''
        U1((lamda-phi)/2) t;
        CX c,t;
        U3(-theta/2, 0, -(phi+lamda)/2) t;
        CX c,t;
        U3(theta/2, phi, 0) t;
        '''
        pass


class NSGate():
    """Non-linear sign-shift gate"""
    def __init__(self):
        # Parts required
        # 1 laser on
        # 1 laser off
        # 1 phase shifter
        # 3 beam splitters
        # 1
        pass


class INSGate():
    """The inverted non-linear sign-shift gate"""
    def __init__(self):
        self.inputs = {
            1: {'type': 'quantum', 'state': 'any'},
            2: {'type': 'laser', 'state': 1},
            3: {'type': 'laser', 'state': 0},
        }
        self.theta = {
            1: 22.5,
            2: 65.5302,
            3: -22.5,
        }
        self.phi = {
            1: 0,
            2: 0,
            3: 0,
            4: pi,
        }
        self.outputs = {
            '1': {'type': 'quantum', 'state': 'any'},
            '2': {'type': 'electric', 'state': 1},
            '3': {'type': 'electric', 'state': 0},
        }

    def describe_gate(self):
        """Describes the gate"""
        print("Gate inputs: ", self.inputs)
        print("Gate outputs: ", self.outputs)

    def _internals(self):
        """Defines the internal circuitry of the gate"""
        # 1 passes through phase shifter and into beam splitter 2.
        # 2 passes into beam splitter 1
        # 3 passes into beam splitter 1
        # bs1 passes into bs2 & bs3
        # bs2 passes into out1 & bs2
        # bs3 passes into out2 & 3
        pass

    def _build_circuit(self):
        pass
        '''
        self.circuit = {
            1: {
                1: phase
        pass'''


class GateDesigner():

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.qubits = {
            'Q1': {
                "IO": 'I',
                "Start": "0",
                "End": "1",
                "Out": "Q2"
            },
            'Q2': []}
        pass
