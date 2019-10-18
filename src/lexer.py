from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Specification
        self.lexer.add('OPENQ', r'(?i)OPENQASM')
        # Includes
        self.lexer.add('INCLUDE', r'(?i)include')
        # Logic
        self.lexer.add('OPAQUE', r'(?i)opaque')
        self.lexer.add('BARRIER', r'(?i)barrier')
        self.lexer.add('IF', r'(?i)if')
        self.lexer.add('MEASURE', r'(?i)measure')
        self.lexer.add('RESET', r'(?i)reset')
        # Registers
        self.lexer.add('QREG', r'(?i)qreg')
        self.lexer.add('CREG', r'(?i)creg')
        self.lexer.add('GATE', r'(?i)gate')
        # Punctuation
        self.lexer.add('PAREN_OPEN', r'\(')
        self.lexer.add('PAREN_CLOSE', r'\)')
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')
        self.lexer.add('SEMI_COLON', r';')
        self.lexer.add('COLON', r':')
        self.lexer.add('DASH', r'-')
        self.lexer.add('UNDER_SCORE', r'_')
        self.lexer.add('COMMA', r',')
        self.lexer.add('QUOTE', r'"')
        self.lexer.add('QUOTE', r"'")
        # Gates
        self.lexer.add('U3', r'(?i)u3')
        self.lexer.add('U2', r'(?i)u2')
        self.lexer.add('U1', r'(?i)u1')
        self.lexer.add('CX', r'(?i)CX')
        self.lexer.add('I', r'(?i)i')
        self.lexer.add('X', r'(?i)x')
        self.lexer.add('Y', r'(?i)y')
        self.lexer.add('Z', r'(?i)z')
        self.lexer.add('H', r'(?i)h')
        self.lexer.add('SDG', r'(?i)sdg')
        self.lexer.add('TDG', r'(?i)tdg')
        self.lexer.add('S', r'(?i)s a')
        self.lexer.add('T', r'(?i)t a')
        self.lexer.add('RX', r'(?i)rx')
        self.lexer.add('RZ', r'(?i)rz')
        self.lexer.add('RY', r'(?i)ry')
        self.lexer.add('CZ', r'(?i)cz')
        self.lexer.add('CY', r'(?i)zy')
        self.lexer.add('CH', r'(?i)CH')
        self.lexer.add('CCX', r'(?i)ccx')
        self.lexer.add('CRZ', r'(?i)crz')
        self.lexer.add('CU1', r'(?i)cu1')
        self.lexer.add('CU3', r'(?i)cu3')
        # Math
        self.lexer.add('PLUS', r'\+')
        self.lexer.add('MINUS', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('POW', r'\^')
        self.lexer.add('PI', r'(?i)pi')
        self.lexer.add('SIN', r'(?i)sin')
        self.lexer.add('COS', r'(?i)cos')
        self.lexer.add('TAN', r'(?i)tan')
        self.lexer.add('EXP', r'(?i)exp')
        self.lexer.add('LN', r'(?i)ln')
        self.lexer.add('SQRT', r'(?i)sqrt')
        #Chars
        self.lexer.add('CHAR', r'(?i)[a-z]')
        self.lexer.add('ID', r'[a-z][A-Za-z0-9_]*')
        # Numbers
        self.lexer.add('NUMBER', r'\d+')
        self.lexer.add('REAL', r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?')
        self.lexer.add('NNINT', r'[1-9]+[0-9]*|0')

        # Other Chars
        self.lexer.ignore('\s+')
        self.lexer.ignore(r'\//.*//')
        self.lexer.ignore(r'\\\.*\\')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
