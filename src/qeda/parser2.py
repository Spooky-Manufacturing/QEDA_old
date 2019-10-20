from rply import ParserGenerator

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
            print('Setting main')
            return p[0]

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
            pass

        @self.parser_generator.production('gatedecl : GATE id idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN PAREN_CLOSE idlist OPEN_BRACE')
        @self.parser_generator.production('gatedecl : GATE id PAREN_OPEN idlist PAREN_CLOSE idlist OPEN_BRACE')
        def gatedecl(p):
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
            pass

        @self.parser_generator.production('uop : U PAREN_OPEN explist PAREN_CLOSE argument SEMI_COLON')
        @self.parser_generator.production('uop : CX argument COMMA argument SEMI_COLON')
        @self.parser_generator.production('uop : int anylist SEMI_COLON')
        @self.parser_generator.production('uop : int PAREN_OPEN PAREN_CLOSE anylist SEMI_COLON')
        @self.parser_generator.production('uop : int PAREN_OPEN explist PAREN_CLOSE anylist SEMI_COLON')
        def uop(p):
            print('setting uop')
            if p[0].name == 'U':
                print('U gate!')
                return p
            elif p[0].name == 'CX':
                print('Controlled Gate!')
                return p
            pass

        @self.parser_generator.production('anylist : idlist')
        @self.parser_generator.production('anylist : mixedlist')
        def anylist(p):
            pass

        @self.parser_generator.production('idlist : id COMMA id')
        @self.parser_generator.production('idlist : idlist COMMA id')
        def idlist(p):
            return p[0]

        @self.parser_generator.production('mixedlist : id OPEN_BRACKET int CLOSE_BRACKET')
        @self.parser_generator.production('mixedlist : mixedlist COMMA id')
        @self.parser_generator.production('mixedlist : mixedlist COMMA id OPEN_BRACKET int CLOSE_BRACKET')
        @self.parser_generator.production('mixedlist : idlist COMMA id OPEN_BRACKET int CLOSE_BRACKET')
        def mixedlist(p):
            return p[0]

        @self.parser_generator.production('argument : id')
        @self.parser_generator.production('argument : real')
        @self.parser_generator.production('argument : INT')
        def argument(p):
            return p[0]

        @self.parser_generator.production('explist : expression')
        @self.parser_generator.production('explist : explist COMMA expression')
        def explist(p):
            return p[0]

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
            pass

        @self.parser_generator.production('unaryop : SQRT ')
        @self.parser_generator.production('unaryop : SIN ')
        @self.parser_generator.production('unaryop : COS ')
        @self.parser_generator.production('unaryop : TAN ')
        @self.parser_generator.production('unaryop : EXP ')
        @self.parser_generator.production('unaryop : LN ')
        def unaryop(p):
            return p[0]

        @self.parser_generator.production('id : ID ')
        def id(p):
            print('setting id', p[0].value)
            return p[0]

        @self.parser_generator.production('int : INT')
        def nnint(p):
            print('setting int', p[0].value)
            return p[0]
        @self.parser_generator.production('real : REAL')
        def real(p):
            print('setting float', p[0].value)
            return p[0]

        @self.parser_generator.error
        def error_handle(token):
            '''"Dirty" error handling'''
            print(token)
            raise ValueError(token)

    def get_parser(self):
        '''Returns a parser generator object'''
        return self.parser_generator.build()

