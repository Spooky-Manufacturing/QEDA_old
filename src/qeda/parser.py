import importlib
from rply import ParserGenerator
from qeda.qast import *


class Parser():

    def __init__(self, verbose=False):
        self.verbose = str(verbose).lower()
        self.setup_verbosity()
        self.parser_generator = ParserGenerator(
            ['$end', 'OPENQASM', 'INCLUDE', 'OPAQUE', 'BARRIER', 'IF', 'MEASURE',
             'RESET', 'QREG', 'CREG', 'GATE', 'PAREN_OPEN', 'PAREN_CLOSE', 'STRING',
             'OPEN_BRACKET', 'CLOSE_BRACKET', 'OPEN_BRACE', 'CLOSE_BRACE',
              'SEMI_COLON', 'COLON', 'DASH', 'UNDER_SCORE', 'COMMA', 'QUOTE',
              'U', 'CX', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'PI', 'SIN', 
              'COS', 'TAN', 'EXP', 'LN', 'SQRT', 'ASSIGN_TO', 'EQU', 'ID', 'INT', 'REAL']

        )
    def setup_verbosity(self):
        global V
        V = getattr(importlib.import_module("qeda.verbose", self.verbose), self.verbose)
        V("Verbosity setup complete")
    
    def parse(self):

        @self.parser_generator.production('main : OPENQASM real SEMI_COLON program')
        @self.parser_generator.production('main : OPENQASM real SEMI_COLON include program')
        def main(p):
            V("Creating Main")
            V("QCODE: {}".format(QCODE))
            return QCODE

        @self.parser_generator.production('include : INCLUDE STRING SEMI_COLON')
        def include(p):
            V("Including file {}".format(p[1]))
            return p[0]

        @self.parser_generator.production('program : statement')
        @self.parser_generator.production('program : program statement')
        def program(p):
            V("Creating program!")
            pass

        @self.parser_generator.production('statement : decl')
        @self.parser_generator.production('statement : gatedecl goplist CLOSE_BRACE')
        @self.parser_generator.production('statement : gatedecl CLOSE_BRACE')
        @self.parser_generator.production('statement : OPAQUE id idlist SEMI_COLON')
        @self.parser_generator.production('statement : OPAQUE id PAREN_OPEN PAREN_CLOSE idlist SEMI_COLON')
        @self.parser_generator.production('statement : OPAQUE id PAREN_OPEN idlist PAREN_CLOSE idlist SEMI_COLON')
        @self.parser_generator.production('statement : qop')
        @self.parser_generator.production('statement : IF PAREN_OPEN id EQU EQU int PAREN_CLOSE qop')
        @self.parser_generator.production('statement : BARRIER anylist SEMI_COLON')
        def statement(p):
            V("Creating statement!")
            pass

        @self.parser_generator.production('decl : QREG id OPEN_BRACKET int CLOSE_BRACKET SEMI_COLON')
        @self.parser_generator.production('decl : CREG id OPEN_BRACKET int CLOSE_BRACKET SEMI_COLON')
        def decl(p):
            V("Declaring register {} id {}".format(p[0].name, p[1].value))
            if p[0].name == 'QREG':
                V("Creating quantum register")
            elif p[0].name == 'CREG':
                V("Creating classical register")
            pass

        @self.parser_generator.production('gatedecl : GATE id idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN PAREN_CLOSE idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN idlist PAREN_CLOSE idlist OPEN_BRACE')
        def gatedecl(p):
            V([x for x in p])
            V('Declaring GATE: {}'.format(p[1].value))
            if 'list' in str(type(p[2])):
                return GateDecl(p[1].value, args=p[2])
            elif p[2].value == 'PAREN_OPEN':
                if len(p) == 7:
                    return GateDecl(p[1].value, args=p[3])
                return GateDecl(p[1].value, control=p[3])

        @self.parser_generator.production('goplist : uop')
        @self.parser_generator.production('goplist : BARRIER idlist SEMI_COLON')
        @self.parser_generator.production('goplist : goplist uop')
        @self.parser_generator.production('goplist : goplist BARRIER idlist SEMI_COLON')
        def goplist(p):
            pass

        @self.parser_generator.production('qop : uop')
        @self.parser_generator.production('qop : MEASURE argument ASSIGN_TO argument SEMI_COLON')
        @self.parser_generator.production('qop : RESET argument SEMI_COLON')
        def qop(p):
           if "Token" in str(type(p[0])):
                V("Token")
                if p[0].name == 'MEASURE':
                    V("MEASURE: {}, {}".format(p[1],p[3]))
                    Measure(p[1])
                    V("Measure complete")
                elif p[0].name == 'RESET':
                    V("RESET")
           else:
                return p[0]

        @self.parser_generator.production('uop : U PAREN_OPEN explist PAREN_CLOSE argument SEMI_COLON')
        @self.parser_generator.production('uop : CX argument COMMA argument SEMI_COLON')
        @self.parser_generator.production('uop : CX anylist SEMI_COLON')
        @self.parser_generator.production('uop : int anylist SEMI_COLON')
        @self.parser_generator.production('uop : int PAREN_OPEN PAREN_CLOSE anylist SEMI_COLON')
        @self.parser_generator.production('uop : int PAREN_OPEN explist PAREN_CLOSE anylist SEMI_COLON')
        @self.parser_generator.production('uop : id anylist SEMI_COLON') # Adds support for custom gates: ccx a,b,c;
        @self.parser_generator.production('uop : id id SEMI_COLON') # supports: y b;
        @self.parser_generator.production('uop : id id OPEN_BRACKET int CLOSE_BRACKET SEMI_COLON') # supports X a[1];
        @self.parser_generator.production('uop : id PAREN_OPEN int PAREN_CLOSE SEMI_COLON') # Supports X(0);
        def uop(p):
            V('uop', p)
            if p[0].name in ('U', 'u'):
                V('U gate!')
                return p
            elif p[0].name in ('cx', 'CX'):
                V("CX Gate")
                if len(p) == 5:
                    return CX(p[1],p[3])
                else:
                    return CX(p[0][0],p[0][1])
            elif p[0].name == 'ID':
                V('a',p)
                if p[0].value.lower() == 'h':
                    V("Hadamard!")
                    return H(p[2])
                elif p[0].value.lower() == 'i':
                    V("Identity!")
                    return I(p[2])
                elif p[0].value.lower() == 's':
                    V("S Gate")
                    return S(p[2])
                elif p[0].value.lower() == 'sdg':
                    V("SDG Gate")
                    return SDG(p[2])
                elif p[0].value.lower() == 't':
                    V("T Gate")
                    return T(p[2])
                elif p[0].value.lower() == 'tdg':
                    V("TDG Gate")
                    return TDG(p[2])
                elif p[0].value.lower() == 'x':
                    V("X Gate")
                    return X(p[2])
                elif p[0].value.lower() == 'y':
                    V("Y Gate")
                    return Y(p[2])
                elif p[0].value.lower() == 'z':
                    V("Z Gate")
                    return Z(p[2])
                elif p[0].value.lower() == 'rx':
                    V("RX Gate")
                    return RX(p[2])
                elif p[0].value.lower() == 'ry':
                    V("RY Gate")
                    return RY(p[2])
                elif p[0].value.lower() == 'rz':
                    V("RZ Gate")
                    return RZ(p[2])
                else:
                    V(p[0])
                return p
            pass

        @self.parser_generator.production('anylist : idlist')
        @self.parser_generator.production('anylist : mixedlist')
        def anylist(p):
            x = []
            if type(p[0]) == list:
                V("anylist list", p[0])
                x = [x for x in p[0]]
                V("anylist list res", x)
            elif 'token' in str(type(p[0])):
                V('anylist token', p[0])
                x = [x for x in p]
            return x

        @self.parser_generator.production('idlist : id COMMA id')
        @self.parser_generator.production('idlist : idlist COMMA id')
        def idlist(p):
            x = []
            if type(p[0]) == list:
                V("idlist list", p[0])
                x = [x for x in p[0]]
                x.append(p[2])
                V('idlist list res', x)
            elif 'token' in str(type(p[0])):
                V('idlist token', p[0])
                x = [p[0], p[2]]
                V('idlist token res', x)
            return x
        
        @self.parser_generator.production('mixedlist : id OPEN_BRACKET int CLOSE_BRACKET')
        @self.parser_generator.production('mixedlist : mixedlist COMMA id')
        @self.parser_generator.production('mixedlist : mixedlist COMMA id OPEN_BRACKET int CLOSE_BRACKET')
        @self.parser_generator.production('mixedlist : idlist COMMA id OPEN_BRACKET int CLOSE_BRACKET')
        def mixedlist(p):
            if 'token' in str(type(p[0])):
                x = [{ 'name': p[0], 'val': p[2]}]
            elif type(p[0]) == list:
                if len(p) == 3:
                    x = [x for x in p[0]]
                    x.append(p[2])
                else:
                    x = [x for x in p[0]]
                    x.append({
                        'name': [2],
                        'val': [4]})
            V('mixedlist', x)
            return x

        @self.parser_generator.production('argument : id')
        @self.parser_generator.production('argument : real')
        @self.parser_generator.production('argument : int')
        @self.parser_generator.production('argument : anylist')
        def argument(p):
            V('arg', p)
            return p[0]

        @self.parser_generator.production('explist : expression')
        @self.parser_generator.production('explist : explist COMMA expression')
        def explist(p):
            if 'expression' in type(p[0]):
                x = [x for x in p]
            elif type(p[0]) == list:
                x = p[0]
                x.append(p[2])
            return x

        @self.parser_generator.production('expression : real')
        @self.parser_generator.production('expression : int')
        @self.parser_generator.production('expression : PI')
        @self.parser_generator.production('expression : id')
        @self.parser_generator.production('expression : expression PLUS expression')
        @self.parser_generator.production('expression : expression MINUS expression')
        @self.parser_generator.production('expression : expression MUL expression')
        @self.parser_generator.production('expression : expression DIV expression')
        @self.parser_generator.production('expression : expression POW expression')
        @self.parser_generator.production('expression : PAREN_OPEN expression PAREN_CLOSE')
        @self.parser_generator.production('expression : unaryop PAREN_OPEN expression PAREN_CLOSE')
        def expression(p):
            V('expression', p)
            return p
            pass

        @self.parser_generator.production('unaryop : SQRT ')
        @self.parser_generator.production('unaryop : SIN ')
        @self.parser_generator.production('unaryop : COS ')
        @self.parser_generator.production('unaryop : TAN ')
        @self.parser_generator.production('unaryop : EXP ')
        @self.parser_generator.production('unaryop : LN ')
        def unaryop(p):
            V('unaryop', p)
            return p[0]

        @self.parser_generator.production('id : ID ')
        def id(p):
            V([p[x].value for x in range(len(p))])
            V('setting id', p[0].value)
            return p[0]

        @self.parser_generator.production('int : INT')
        def nnint(p):
            V('setting int', p[0].value)
            return Int(p[0].value)

        @self.parser_generator.production('real : REAL')
        def real(p):
            V('setting float', p[0].value)
            return p[0]

        @self.parser_generator.error
        def error_handle(token):
            '''"Dirty" error handling'''
            V(token)
            raise ValueError(token)

    def get_parser(self):
        '''Returns a parser generator object'''
        return self.parser_generator.build()

