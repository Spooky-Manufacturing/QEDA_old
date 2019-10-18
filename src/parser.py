from rply import ParserGenerator
from qast import OpenQASM, Number, Char, I, S, SDG, T, TDG, X, Y, Z
from qast import RX, RY, RZ, CX, End, CYGate, CZGate, CHGate, CCXGate
from qast import Measure


class Parser():
    def __init__(self):
        self.parser_generator = ParserGenerator(
            ['$end', 'OPENQ', 'INCLUDE', 'OPAQUE', 'BARRIER', 'IF', 'MEASURE',
             'RESET', 'QREG', 'CREG', 'GATE', 'PAREN_OPEN', 'PAREN_CLOSE',
             'OPEN_BRACKET', 'CLOSE_BRACKET', 'SEMI_COLON', 'COLON', 'DASH',
             'UNDER_SCORE', 'COMMA', 'QUOTE', 'U3', 'U2', 'U1', 'CX', 'I', 'X', 'Y',
             'Z', 'H', 'SDG', 'TDG', 'S', 'T', 'RX', 'RZ', 'RY', 'CZ', 'CY',
             'CH', 'CCX', 'CRZ', 'CU1', 'CU3', 'PLUS', 'MINUS', 'MUL', 'DIV',
             'POW', 'PI', 'SIN', 'COS', 'TAN', 'EXP', 'LN', 'SQRT',
             'CHAR', 'ID', 'NUMBER', 'REAL', 'NNINT']

        )

    def parse(self):

        @self.parser_generator.production('main : expression')
        def main(p):
            '''Main function'''
            return p[0]

        # Check version of OpenQASM (ToDo)
        @self.parser_generator.production('expression : OPENQ NUMBER expression')
        @self.parser_generator.production('expression : OPENQ REAL expression')
        def prog(p):
            '''Defines the version of qasm to use'''
            x = OpenQASM(1)
            return x

        @self.parser_generator.production('expression : INCLUDE expression SEMI_COLON')
        def include(p):
            '''Defines the INCLUDE command
            Will be implemented.
            Priority: LOW
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('''expression : GATE expression PAREN_OPEN
expression PAREN_CLOSE expression OPEN_BRACKET expression CLOSE_BRACKET''')
        def gate(p):
            '''Defines the QASM Gate Definition command.
            Will be implemented.
            Priority: MEDIUM
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('''expression : OPAQUE expression PAREN_OPEN
expression PAREN_CLOSE expression OPEN_BRACKET expression CLOSE_BRACKET''')
        def opaque(p):
            '''Defines the OPAQUE command
            Unlikely to be implemented.
            Priority: LOW
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('expression : BARRIER')
        def barrier(p):
            '''Defines the BARRIER command.
            Unlikely to be implemented.
            Priority: LOW
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('expression : IF')
        def iF(p):
            '''Defines the IF command
            Will be implemented.
            Prioty: MEDIUM
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('expression : MEASURE')
        def measure(p):
            '''Defines the measurement command and places MEASURE gate.
            Will be implemented.
            Priority: HIGH
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('expression : RESET')
        def reset(p):
            '''Defines the reset command.
            unlikely to be implemented.
            Priority: LOW
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('''expression : QREG expression OPEN_BRACKET
expression CLOSE_BRACKET SEMI_COLON''')
        def qreg(p):
            '''Defines the Quatum Register.
            Will be implemented when physically possible.
            Priority: LOW
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        @self.parser_generator.production('''expression : CREG expression OPEN_BRACKET
expression CLOSE_BRACKET SEMI_COLON''')
        def creg(p):
            '''Defines a binary register.
            Will be implemented
            Priority: MEDIUM
            '''
            raise NotImplementedError('Error', p[0], ' not implemented')

        # Gates
        @self.parser_generator.production('''expression : H PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def h(p):
            '''Defines the Hadamard Gate

            Returns the master dict with gate appended to chosen qubit.
            '''
            print("H")
            print(p[0:4])
            return H(p[2])

        @self.parser_generator.production('''expression : I PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')

        def i(p):
            '''Defines the identity gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print("I")
            return I(p[2])

        @self.parser_generator.production('''expression : S PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def s(p):
            '''Defines the S Gate

            Returns the master dict with gate appended to chosen qubit.
            '''
            print("S")
            return S(p[2])

        @self.parser_generator.production('''expression : SDG PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def sdg(p):
            '''Defines the SDG Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print("SDG")
            return SDG(p[2])

        @self.parser_generator.production('''expression : T PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')

        def t(p):
            '''Defines the T Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print("T")
            return T(p[2])

        @self.parser_generator.production('''expression : TDG PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def tdg(p):
            '''Defines the TDG Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print("TDG")
            return TDG(p[2])

        @self.parser_generator.production('''expression : X PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')

        def x(p):
            '''Defines the Pauli-X Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print("X")
            return X(p[2])

        @self.parser_generator.production('''expression : Y PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def y(p):
            '''Defines the Pauli-Y Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print('Y')
            return Y(p[2])

        @self.parser_generator.production('''expression : Z PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def z(p):
            '''Defines the Pauli-Z Gate

            Returns the master dict with gate appended to chosen qubit
            '''
            print('Z')
            return Z(p[2])

        @self.parser_generator.production('''expression : RX PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def rx(p):
            '''Defines the RX gates.

            Performs a rotation around the X axis of a qubit
            Returns the master dict with RX gate appended to the chosen qubit.
            '''
            print('RX')
            return RX(p[2])

        @self.parser_generator.production('''expression : RY PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def ry(p):
            '''Defines the RY Gates.

            Performs a rotation around the Y axis of a qubit.
            Returns the master dict with RY gate appended to the chosen qubit.
            '''
            print('RY')
            return RY(p[2])

        @self.parser_generator.production('''expression : RZ PAREN_OPEN expression
PAREN_CLOSE SEMI_COLON expression''')
        def rz(p):
            '''Defines the RZ Gate

            Performs a rotation around the Z axis (phase).
            If a positive Z rotation occurs, appends a negative phase shift gate to all
            other qubits. If a negative rotation occurs, appends the negative phase shift
            to chosen qubit.
            Returns the master dict.
            '''
            print('RZ')
            return RZ(p[2])

        @self.parser_generator.production('''expression : CX expression COMMA
expression SEMI_COLON expression''')
        def cx(p):
            '''Defines the Controlled-Not Gate

            Returns the master dict with CX gate appended to target and control
            qubits.
            '''
            print('CX')
            return CX(p[1], p[3])

        @self.parser_generator.production('''expression : CY expression COMMA
expression SEMI_COLON expression''')
        def cy(p):
            '''Defines the Controlled-Y Gate

            Returns the master dict with CY Gate appended to target and control
            qubits.
            '''
            print("CY")
            return CYGate(p[1], p[3])

        @self.parser_generator.production('''expression : CZ expression COMMA
expression SEMI_COLON expression''')
        def cz(p):
            '''Defines the Controlled-Z Gate

            Returns the master dict with CZ Gate appended to target and control
            qubits.
            '''
            print("CZ")
            return CZGate(p[1], p[3])

        @self.parser_generator.production('''expression : CH expression COMMA
expression SEMI_COLON expression''')
        def ch(p):
            '''Defines the Controlled Hadamard Gate

            Returns the master dict with CH Gate appended to target and control
            qubits.
            '''
            print("CH")
            return CHGate(p[1], p[3])

        @self.parser_generator.production('''expression : CCX expression COMMA
expression COMMA expression SEMI_COLON expression''')
        def ccx(p):
            '''Defines the Controlled Controlled Not Gate

            Returns the master dict with CCX appended to target, control 1, and
            control 2 qubits.
            '''
            print("CCX")
            return CCXGate(p[1], [p[3], p[5]])

        # Basic Definitions
        @self.parser_generator.production('expression : NUMBER')
        def number(p):
            '''Defines the number primitive'''
            return Number(p[0].value)

        @self.parser_generator.production('expression : CHAR')
        def char(p):
            '''Defines the character primitive'''
            return Char(p[0].value)

        @self.parser_generator.production('expression : $end')
        def end(p):
            '''Used to finish compiling'''
            return End()

        @self.parser_generator.error
        def error_handle(token):
            '''"Dirty" error handling'''
            raise ValueError(token)

    def get_parser(self):
        '''Returns a parser generator object'''
        return self.parser_generator.build()
