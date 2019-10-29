from rply import ParserGenerator
from qeda.qast import *

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
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
        @self.pg.production('main : expression')
        def main(p):
            return p[0]

        # Check version of OpenQASM (ToDo)
        @self.pg.production('expression : OPENQ NUMBER expression')
        @self.pg.production('expression : OPENQ REAL expression')
        def prog(p):
            x = OpenQASM(1)
            return x

        @self.pg.production('expression : INCLUDE expression SEMI_COLON')
        def include(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : GATE expression PAREN_OPEN expression PAREN_CLOSE expression OPEN_BRACKET expression CLOSE_BRACKET')
        def gate(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : OPAQUE expression PAREN_OPEN expression PAREN_CLOSE expression OPEN_BRACKET expression CLOSE_BRACKET')
        def opaque(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : BARRIER')
        def barrier(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : IF')
        def iF(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : MEASURE')
        def measure(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : RESET')
        def reset(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : QREG expression OPEN_BRACKET expression CLOSE_BRACKET SEMI_COLON')
        def qreg(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        @self.pg.production('expression : CREG expression OPEN_BRACKET expression CLOSE_BRACKET SEMI_COLON')
        def creg(p):
            raise NotImplemented('Error', p[0], ' not implemented')
        # Gates
        @self.pg.production('expression : H PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def h(p):
            print("H")
            print(p[0:4])
            return H(p[2])

        @self.pg.production('expression : I PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def i(p):
            print("I")
            return I(p[2])

        @self.pg.production('expression : S PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def s(p):
            print("S")
            return S(p[2])

        @self.pg.production('expression : SDG PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def sdg(p):
            print("SDG")
            return SDG(p[2])

        @self.pg.production('expression : T PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def t(p):
            print("T")
            return T(p[2])

        @self.pg.production('expression : TDG PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def tdg(p):
            print("TDG")
            return TDG(p[2])

        @self.pg.production('expression : X PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def x(p):
            print("X")
            return X(p[2])

        @self.pg.production('expression : Y PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def y(p):
            print('Y')
            return Y(p[2])

        @self.pg.production('expression : Z PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def z(p):
            print('Z')
            return Z(p[2])

        @self.pg.production('expression : RX PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def rx(p):
            print('RX')
            return RX(p[2])

        @self.pg.production('expression : RY PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def ry(p):
            print('RY')
            return RX(p[2])

        @self.pg.production('expression : RZ PAREN_OPEN expression PAREN_CLOSE SEMI_COLON expression')
        def rz(p):
            print('RZ')
            return RZ(p[2])

        @self.pg.production('expression : CX expression COMMA expression SEMI_COLON expression')
        def cx(p):
            print('CX')
            return CX(p[1],p[3])

        @self.pg.production('expression : CY expression COMMA expression SEMI_COLON expression')
        def cy(p):
            print("CY")
            return CY(p[1],p[3])

        @self.pg.production('expression : CZ expression COMMA expression SEMI_COLON expression')
        def cz(p):
            print("CZ")
            return CZ(p[1],p[3])

        @self.pg.production('expression : CH expression COMMA expression SEMI_COLON expression')
        def ch(p):
            print("CH")
            return CH(p[1],p[3])

        @self.pg.production('expression : CCX expression COMMA expression COMMA expression SEMI_COLON expression')
        def ccx(p):
            print("CCX")
            return CCX(p[1],[p[3],p[5]])
                            
        # Basic Definitions
        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(p[0].value)

        @self.pg.production('expression : CHAR')
        def char(p):
            return Char(p[0].value)

        @self.pg.production('expression : $end')
        def end(p):
            return End()
        
        @self.pg.error
        def error_handle(token):
            raise ValueError(token)
        

    def get_parser(self):
        return self.pg.build()
