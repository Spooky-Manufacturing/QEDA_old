from rply import LexerGenerator

class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Specification
        self.lexer.add('OPENQASM', r'(?i)OPENQASM')
        #String support
        self.lexer.add('STRING', r'".*"')
        self.lexer.add('STRING', r"'.*'")
        # Includes
        self.lexer.add('INCLUDE', r'(?i)include')
        # Logic
        self.lexer.add('OPAQUE', r'(?i)opaque')
        self.lexer.add('BARRIER', r'(?i)barrier')
        self.lexer.add('IF', r'(?i)if')
        self.lexer.add('MEASURE', r'(?i)measure')
        self.lexer.add('RESET', r'(?i)reset')
        self.lexer.add('ASSIGN_TO', r'\-\>')
        # Registers
        self.lexer.add('QREG', r'(?i)qreg')
        self.lexer.add('CREG', r'(?i)creg')
        self.lexer.add('GATE', r'(?i)gate')
        # Gate primitives
        self.lexer.add('U', r'U')
        self.lexer.add('CX', r'(?i)cx')
        # Punctuation
        self.lexer.add('PAREN_OPEN', r'\(')
        self.lexer.add('PAREN_CLOSE', r'\)')
        self.lexer.add('OPEN_BRACKET', r'\[')
        self.lexer.add('CLOSE_BRACKET', r'\]')
        self.lexer.add('OPEN_BRACE', r'\{')
        self.lexer.add('CLOSE_BRACE', r'\}')
        self.lexer.add('SEMI_COLON', r';')
        self.lexer.add('COLON', r':')
        self.lexer.add('DASH', r'-')
        self.lexer.add('UNDER_SCORE', r'_')
        self.lexer.add('COMMA', r',')
        self.lexer.add('QUOTE', r'"')
        self.lexer.add('QUOTE', r"'")
        # Math
        self.lexer.add('EQU', r'\=')
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
        #ID support
        self.lexer.add('ID', r'[a-z][A-Za-z0-9_]*|[A-Z][A-Za-z0-9_]*')
        # Numbers
        self.lexer.add('REAL', r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?')
        self.lexer.add('INT', r'[1-9]+[0-9]*|0')
        # Character support
        #self.lexer.add('CHARS', r'[A-Za-z]*')
        self.lexer.add('DOT', r'\.')


        # Other Chars
        self.lexer.ignore('\s+')
        # Ignore Comments
        self.lexer.ignore(r'\//.*//')
        self.lexer.ignore(r'\\\.*\\')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
