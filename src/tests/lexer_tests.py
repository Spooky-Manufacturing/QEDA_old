import unittest
from context import Lexer

class LexerTests(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer().get_lexer()

    def _get_tokens(self, text):
        return self.lexer.lex(text)

    def _tokens_equ(self, tokens, equals):
        i = 0
        for token in tokens:
            print(token.name, token.value)
            self.assertEqual(token.name, equals[i])
            i += 1

    def test_comments(self):
        # comments should be completely ignored
        text ='//this is a comment in qasm//h1'
        tokens = self._get_tokens(text)
        self._tokens_equ(tokens, ['ID'])
        # Only the H gate should be seen in the above code
        for token in tokens:
            self.assertEqual(token.name, 'ID')

    def test_string(self):
        text1 = "'This is a string'"
        text2 = '"This is also a string"'
        tokens = self._get_tokens(text1)
        equals = ['STRING']
        self._tokens_equ(tokens, equals)
        tokens = self._get_tokens(text2)
        equals = ['STRING']
        self._tokens_equ(tokens, equals)

    def test_specification(self):
        text = 'OPENQASM: 2.0;'
        tokens = self._get_tokens(text)
        equals = ['OPENQASM' , 'COLON', 'REAL', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_include(self):
        text = "include 'qelib.inc';"
        tokens = self._get_tokens(text)
        equals = ['INCLUDE', 'STRING', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_opaque(self):
        text = "opaque test(a, b) q"
        tokens = self._get_tokens(text)
        equals = ['OPAQUE', 'ID', 'PAREN_OPEN', 'ID',
                  'COMMA', 'ID',
                  'PAREN_CLOSE', 'ID']
        self._tokens_equ(tokens, equals)

    def test_barrier(self):
        text = 'barrier q[0],q[1];'
        tokens = self._get_tokens(text)
        equals = ['BARRIER', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'ID', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_if(self):
        text = 'if(c==5) x q[0],q[1];'
        tokens = self._get_tokens(text)
        equals = ['IF', 'PAREN_OPEN', 'ID', 'EQU', 'EQU',
                  'INT', 'PAREN_CLOSE', 'ID', 'ID',
                  'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'COMMA', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_measure(self):
        text = 'measure q -> c'
        tokens = self._get_tokens(text)
        equals = ['MEASURE', 'ID', 'ASSIGN_TO', 'ID']
        self._tokens_equ(tokens, equals)

    def test_reset(self):
        text = 'reset q[0];'
        tokens = self._get_tokens(text)
        equals = ['RESET', 'ID', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_qreg(self):
        text = 'qreg q[5];'
        tokens = self._get_tokens(text)
        equals = ['QREG', 'ID', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_creg(self):
        text = 'creg c[5];'
        tokens = self._get_tokens(text)
        equals = ['CREG', 'ID', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_gate(self):
        text = 'gate u3(t, p, l) q { U(t, p, l) q; }'
        tokens = self._get_tokens(text)
        equals = ['GATE', 'ID', 'PAREN_OPEN',
                  'ID', 'COMMA', 'ID', 'COMMA',
                  'ID', 'PAREN_CLOSE',
                  'ID', 'OPEN_BRACE', 
                  'U', 'PAREN_OPEN', 'ID', 'COMMA',
                  'ID', 'COMMA', 'ID',
                  'PAREN_CLOSE', 'ID', 'SEMI_COLON',
                  'CLOSE_BRACE']
        self._tokens_equ(tokens, equals)

    def test_full_script(self):
        with open('tests/repetition_code_syndrome_test.qasm', 'r') as f:
            text = ''.join([x.rstrip() for x in f.readlines()])
        tokens = self._get_tokens(text)
        equals = ['OPENQ', 'FLOAT', 'SEMI_COLON',
                  'INCLUDE', 'STRING', 'SEMI_COLON',
                  'QREG', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON', 'QREG',
                  'ID', 'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'SEMI_COLON', 'CREG', 'ID',
                  'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'SEMI_COLON', 'GATE', 'ID',
                  'ID', 'INT', 'COMMA', 'ID', 'COMMA',
                  'ID', 'INT', 'COMMA', 'ID', 'INT',
                  'COMMA', 'ID', 'INT', 'OPEN_BRACE', 'CX',
                  'ID', 'INT', 'COMMA', 'ID', 'INT', 'SEMI_COLON',
                  'CX', 'ID', 'INT', 'COMMA',
                  'ID', 'INT', 'SEMI_COLON', 'CNOT', 'ID',
                  'INT', 'COMMA', 'ID', 'INT', 'SEMI_COLON',
                  'CX', 'ID', 'INT', 'COMMA', 'ID', 'INT',
                  'SEMI_COLON', 'CLOSE_BRACE', 'X', 'ID',
                  'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET', 'SEMI_COLON',
                  'BARRIER', 'ID', 'SEMI_COLON',
                  'ID', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'ID', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON', 'ID','ID', 'ASSIGN_TO',
                  'ID', 'SEMI_COLON']

        

              
if __name__ == '__main__':
    unittest.main()
