from rply import ParserGenerator
from qeda.qast import *
from qeda.schema import SchemaBuilder
from qeda.pcb import PCBBuilder

class Parser():

    def __init__(self):
        self.parser_generator = ParserGenerator(
            ['$end', 'OPENQASM', 'INCLUDE', 'OPAQUE', 'BARRIER', 'IF', 'MEASURE',
             'RESET', 'QREG', 'CREG', 'GATE', 'PAREN_OPEN', 'PAREN_CLOSE', 'STRING',
             'OPEN_BRACKET', 'CLOSE_BRACKET', 'OPEN_BRACE', 'CLOSE_BRACE',
              'SEMI_COLON', 'COLON', 'DASH', 'UNDER_SCORE', 'COMMA', 'QUOTE',
              'U', 'CX', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'PI', 'SIN', 
              'COS', 'TAN', 'EXP', 'LN', 'SQRT', 'ASSIGN_TO', 'EQU', 'ID', 'INT', 'REAL']

        )

    def parse(self):

        @self.parser_generator.production('main : OPENQASM real SEMI_COLON program')
        @self.parser_generator.production('main : OPENQASM real SEMI_COLON include program')
        def main(p):
            print("Creating main")
            print("QCODE: {}".format(qcode))
            SchemaBuilder(qcode)
            PCBBuilder(qcode)
            return OpenQASM(real)

        @self.parser_generator.production('include : INCLUDE STRING SEMI_COLON')
        def include(p):
            print("Including file")
            return p[0]

        @self.parser_generator.production('program : statement')
        @self.parser_generator.production('program : program statement')
        def program(p):
            print("Creating program!")
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
            print("Creating statement!")
            pass

        @self.parser_generator.production('decl : QREG id OPEN_BRACKET int CLOSE_BRACKET SEMI_COLON')
        @self.parser_generator.production('decl : CREG id OPEN_BRACKET int CLOSE_BRACKET SEMI_COLON')
        def decl(p):
            print("Declaring register {} id {}".format(p[0].name, p[1].value))
            if p[0].name == 'QREG':
                print("Creating quantum register")
            elif p[0].name == 'CREG':
                print("Creating classical register")
            pass

        @self.parser_generator.production('gatedecl : GATE id idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN PAREN_CLOSE idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN idlist PAREN_CLOSE idlist OPEN_BRACE')
        def gatedecl(p):
            if p[2].value == 'PAREN_OPEN':
                if len(p) == 7:
                    GateDecl(p[1].value, args=p[3])
                GateDecl(p[1].value, control=p[3])
            elif list in str(type(p[2])):
                GateDecl(p[1].value, args=p[2])
            print('Declaring GATE: {}'.format(p[1].value))
            pass

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
            if 'token' in str(type(p[0])):
                if p[0].name == 'MEASURE':
                    print("MEASURE")
                elif p[0].name == 'RESET':
                    print("RESET")
            else:
                return p[0]
            pass

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
            print('uop', p[1])
            if p[0].name in ('U', 'u'):
                print('U gate!')
                return p
            elif p[0].name == 'ID':
                print('a',p)
                if p[0].value in ('CCX', 'ccx'):
                    print('Controlled Controlled Gate!')
                elif p[0].value.lower() == 'h':
                    print("Hadamard!")
                    return H(p[2])
                elif p[0].value.lower() == 'i':
                    print("Identity!")
                    return I(p[2])
                elif p[0].value.lower() == 's':
                    print("S Gate")
                    return S(p[2])
                elif p[0].value.lower() == 'sdg':
                    print("SDG Gate")
                    return SDG(p[2])
                elif p[0].value.lower() == 't':
                    print("T Gate")
                    return T(p[2])
                elif p[0].value.lower() == 'tdg':
                    print("TDG Gate")
                    return TDG(p[2])
                elif p[0].value.lower() == 'x':
                    print("X Gate")
                    return X(p[2])
                elif p[0].value.lower() == 'y':
                    print("Y Gate")
                    return Y(p[2])
                elif p[0].value.lower() == 'z':
                    print("Z Gate")
                    return Z(p[2])
                elif p[0].value.lower() == 'rx':
                    print("RX Gate")
                    return RX(p[2])
                elif p[0].value.lower() == 'ry':
                    print("RY Gate")
                    return RY(p[2])
                elif p[0].value.lower() == 'rz':
                    print("RZ Gate")
                    return RZ(p[2])
                else:
                    print(p[0])
                return p
            pass

        @self.parser_generator.production('anylist : idlist')
        @self.parser_generator.production('anylist : mixedlist')
        def anylist(p):
            x = []
            if type(p[0]) == list:
                print("anylist list", p[0])
                x = [x for x in p[0]]
                print("anylist list res", x)
            elif 'token' in str(type(p[0])):
                print('anylist token', p[0])
                x = [x for x in p]
            return x

        @self.parser_generator.production('idlist : id COMMA id')
        @self.parser_generator.production('idlist : idlist COMMA id')
        def idlist(p):
            x = []
            if type(p[0]) == list:
                print("idlist list", p[0])
                x = [x for x in p[0]]
                x.append(p[2])
                print('idlist list res', x)
            elif 'token' in str(type(p[0])):
                print('idlist token', p[0])
                x = [p[0], p[2]]
                print('idlist token res', x)
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
            print('mixedlist', x)
            return x

        @self.parser_generator.production('argument : id')
        @self.parser_generator.production('argument : real')
        @self.parser_generator.production('argument : INT')
        @self.parser_generator.production('argument : anylist')
        def argument(p):
            print('arg', p)
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
            print('expression', p)
            return p
            pass

        @self.parser_generator.production('unaryop : SQRT ')
        @self.parser_generator.production('unaryop : SIN ')
        @self.parser_generator.production('unaryop : COS ')
        @self.parser_generator.production('unaryop : TAN ')
        @self.parser_generator.production('unaryop : EXP ')
        @self.parser_generator.production('unaryop : LN ')
        def unaryop(p):
            print('unaryop', p)
            return p[0]

        @self.parser_generator.production('id : ID ')
        def id(p):
            print([p[x].value for x in range(len(p))])
            print('setting id', p[0].value)
            return p[0]

        @self.parser_generator.production('int : INT')
        def nnint(p):
            print('setting int', p[0].value)
            return Int(p[0].value)
        @self.parser_generator.production('real : REAL')
        def real(p):
            print('setting float', p[0].value)
            return p[0]

        @self.parser_generator.production('main : $end')
        def end(p):
            return p[0]

        @self.parser_generator.error
        def error_handle(token):
            '''"Dirty" error handling'''
            print(token)
            raise ValueError(token)

    def get_parser(self):
        '''Returns a parser generator object'''
        return self.parser_generator.build()

