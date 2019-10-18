import unittest
import sys
sys.path.insert(0,'..')
from lexer import Lexer

class LexerTests(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer().get_lexer()
        pass

    def _get_tokens(self, text):
        return [x for x in self.lexer.lex(text)]

    def _tokens_equ(self, tokens, equals):
        for i in range(len(tokens)):
            self.assertEqual(tokens[i].name, equals[i])
        
    def test_chars(self):
        upperChars = ''.join(
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
             "k", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
             "U", "V", "W", "X", "Y", "Z"])
        lowerChars = ''.join([x.lower() for x in upperChars])
        chars = upperChars + lowerChars
        tokens = self.lexer.lex(chars)
        for token in tokens:
            self.assertEqual(token.name, 'CHAR')
            self.assertEqual(token.value, chars[token.source_pos.idx])

    def test_comments(self):
        # comments should be completely ignored
        text ='//this is a comment in qasm//H '
        tokens = self._get_tokens(text)
        # Only the H gate should be seen in the above code
        for token in tokens:
            self.assertEqual(token.name, 'H')
        
    def test_specification(self):
        text = 'OPENQASM: 2.0;'
        tokens = self._get_tokens(text)
        equals = ['OPENQ' , 'COLON', 'SPACE', 'FLOAT', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_include(self):
        text = "include 'qelib.inc';"
        tokens = self._get_tokens(text)
        equals = ['INCLUDE', 'SPACE', 'STRING', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_opaque(self):
        text = "opaque test(a, b) q"
        tokens = self._get_tokens(text)
        equals = ['OPAQUE', 'SPACE', 'CHAR','CHAR',
                  'CHAR','CHAR', 'PAREN_OPEN', 'CHAR',
                  'COMMA', 'SPACE', 'CHAR',
                  'PAREN_CLOSE', 'SPACE', 'CHAR']
        self._tokens_equ(tokens, equals)

    def test_barrier(self):
        text = 'barrier q[0],q[1];'
        tokens = self._get_tokens(text)
        equals = ['BARRIER', 'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_IF(self):
        text = 'if(c==5) X q[0],q[1];'
        tokens = self._get_tokens(text)
        equals = ['IF', 'PAREN_OPEN', 'CHAR', 'EQU', 'EQU',
                  'INT', 'PAREN_CLOSE', 'SPACE', 'X', 'CHAR',
                  'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'COMMA', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_measure(self):
        text = 'measure q -> c'
        tokens = self._get_tokens(text)
        equals = ['MEASURE', 'SPACE', 'CHAR', 'SPACE',
                  'ASSIGN_TO', 'SPACE', 'CHAR']
        self._tokens_equ(tokens, equals)
        
    def test_reset(self):
        text = 'reset q[0];'
        tokens = self._get_tokens(text)
        equals = ['RESET', 'SPACE', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_qreg(self):
        text = 'qreg q[5];'
        tokens = self._get_tokens(text)
        equals = ['QREG', 'SPACE', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_creg(self):
        text = 'creg c[5];'
        tokens = self._get_tokens(text)
        equals = ['CREG', 'SPACE', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_gate(self):
        text = 'gate u3(t, p, l) q { U(t, p, l) q; }'
        tokens = self._get_tokens(text)
        equals = ['GATE', 'SPACE', 'U3', 'PAREN_OPEN',
                  'CHAR', 'COMMA', 'SPACE', 'CHAR', 'COMMA',
                  'SPACE', 'CHAR', 'PAREN_CLOSE', 'SPACE',
                  'CHAR', 'SPACE', 'OPEN_BRACE', 'SPACE', 
                  'CHAR', 'PAREN_OPEN', 'CHAR', 'COMMA',
                  'SPACE', 'CHAR', 'COMMA', 'SPACE', 'CHAR',
                  'PAREN_CLOSE', 'SPACE', 'CHAR', 'SEMI_COLON',
                  'SPACE', 'CLOSE_BRACE']
        self._tokens_equ(tokens, equals)


    def test_u3_gate(self):
        text = 'gate u3(t, p, l) q { U(t, p, l) q; }'
        tokens = self._get_tokens(text)
        equals = ['GATE', 'SPACE', 'U3', 'PAREN_OPEN', 'CHAR', 'COMMA',
                  'SPACE', 'CHAR', 'COMMA', 'SPACE', 'CHAR', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'SPACE', 'OPEN_BRACE','SPACE', 'CHAR',
                  'PAREN_OPEN', 'CHAR', 'COMMA','SPACE', 'CHAR', 'COMMA',
                  'SPACE', 'CHAR', 'PAREN_CLOSE','SPACE', 'CHAR',
                  'SEMI_COLON','SPACE',  'CLOSE_BRACE']
        self._tokens_equ(tokens, equals)

    def test_u2_gate(self):
        text = 'gate u3(p, l) q { U(p, l) q; }'
        tokens = self._get_tokens(text)
        equals = ['GATE', 'SPACE', 'U3', 'PAREN_OPEN', 'CHAR',
                  'COMMA', 'SPACE',  'CHAR', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'SPACE', 'OPEN_BRACE',
                  'SPACE', 'CHAR', 'PAREN_OPEN', 'CHAR', 'COMMA',
                  'SPACE', 'CHAR', 'PAREN_CLOSE', 'SPACE',
                  'CHAR', 'SEMI_COLON', 'SPACE', 'CLOSE_BRACE']
        self._tokens_equ(tokens, equals)

    def test_u1_gate(self):
        text = 'gate u1(l) q { U(0,0,l) q; }'
        tokens = self._get_tokens(text)
        equals = ['GATE', 'SPACE', 'U1', 'PAREN_OPEN', 'CHAR',
                  'PAREN_CLOSE', 'SPACE', 'CHAR', 'SPACE',
                  'OPEN_BRACE', 'SPACE', 'CHAR', 'PAREN_OPEN',
                  'INT', 'COMMA', 'INT', 'COMMA', 'CHAR',
                  'PAREN_CLOSE', 'SPACE', 'CHAR', 'SEMI_COLON',
                  'SPACE', 'CLOSE_BRACE']
        self._tokens_equ(tokens, equals)

    def test_i_gate(self):
        text = 'id a;'
        tokens = self._get_tokens(text)
        equals = ['I', 'SPACE', 'CHAR', 'SEMI_COLON']

    def test_h_gate(self):
        text = 'H q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['H', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON',]
        self._tokens_equ(tokens, equals)

    def test_x_gate(self):
        text = 'X q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['X', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_y_gate(self):
        text = 'Y q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['Y', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_Z_gate(self):
        text = 'Z q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['Z', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_s_gate(self):
        text = 'S q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['S', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)
        
    def test_sdg_gate(self):
        text = 'sdg q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['SDG', 'SPACE', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_t_gate(self):
        text = 'T q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['T', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_tdg_gate(self):
        text = 'tdg q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['TDG', 'SPACE', 'CHAR', 'OPEN_BRACKET',
                  'INT', 'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_rx_gate(self):
        text = 'rx(1) q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['RX', 'PAREN_OPEN', 'INT', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_rz_gate(self):
        text = 'rz(1) q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['RZ', 'PAREN_OPEN', 'INT', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_rz_gate(self):
        text = 'rz(1) q[1];'
        tokens = [x for x in self.lexer.lex(text)]
        equals = ['RZ', 'PAREN_OPEN', 'INT', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_cx_gate(self):
        text = 'cx b,c;'
        tokens = self._get_tokens(text)
        equals = ['CX', 'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_cy_gate(self):
        text = 'cy b,c;'
        tokens = self._get_tokens(text)
        equals = ['CY', 'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_cz_gate(self):
        text = 'cz b,c;'
        tokens = self._get_tokens(text)
        equals = ['CZ', 'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_ch_gate(self):
        text = 'ch b,c;'
        tokens = self._get_tokens(text)
        equals = ['CH', 'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_crz_gate(self):
        text = 'crz(1) b,c;'
        tokens = self._get_tokens(text)
        equals = ['CRZ', 'PAREN_OPEN', 'INT', 'PAREN_CLOSE',
                  'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_cu1_gate(self):
        text = 'cu1(1) a,b;'
        tokens = self._get_tokens(text)
        equals = ['CU1', 'PAREN_OPEN', 'INT', 'PAREN_CLOSE',
                'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)

    def test_cu3_gate(self):
        text = 'cu3(1,2,3) a,b;'
        tokens = self._get_tokens(text)
        equals = ['CU3', 'PAREN_OPEN', 'INT', 'COMMA',
                'INT', 'COMMA', 'INT', 'PAREN_CLOSE',
                'SPACE', 'CHAR', 'COMMA', 'CHAR', 'SEMI_COLON']
        self._tokens_equ(tokens, equals)


    def test_full_script(self):
        with open('repetition_code_syndrome_test.qasm', 'r') as f:
            text = ''.join([x.rstrip() for x in f.readlines()])
        tokens = self._get_tokens(text)
        equals = ['OPENQ', 'SPACE', 'FLOAT', 'SEMI_COLON',
                  'INCLUDE', 'SPACE', 'STRING', 'SEMI_COLON',
                  'QREG', 'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON', 'QREG', 'SPACE',
                  'CHAR', 'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'SEMI_COLON', 'CREG', 'SPACE', 'CHAR', 'CHAR',
                  'CHAR', 'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET',
                  'SEMI_COLON', 'GATE', 'SPACE', 'CHAR', 'CHAR',
                  'CHAR', 'CHAR', 'CHAR', 'CHAR', 'CHAR', 'CHAR',
                  'SPACE', 'CHAR', 'INT', 'COMMA', 'CHAR', 'INT',
                  'COMMA', 'CHAR', 'INT', 'COMMA', 'CHAR', 'INT',
                  'COMMA', 'CHAR', 'INT', 'OPEN_BRACE', 'CX', 'SPACE',
                  'CHAR', 'INT', 'COMMA', 'CHAR', 'INT', 'SEMI_COLON',
                  'SPACE', 'CX', 'SPACE', 'CHAR', 'INT', 'COMMA',
                  'CHAR', 'INT', 'SEMI_COLON', 'CNOT', 'SPACE', 'CHAR',
                  'INT', 'COMMA', 'CHAR', 'INT', 'SEMI_COLON', 'SPACE',
                  'CX', 'SPACE', 'CHAR', 'INT', 'COMMA', 'CHAR', 'INT',
                  'SEMI_COLON', 'CLOSE_BRACE', 'X', 'SPACE', 'CHAR',
                  'OPEN_BRACKET', 'INT', 'CLOSE_BRACKET', 'SEMI_COLON',
                  'BARRIER', 'SPACE', 'CHAR', 'SEMI_COLON',
                  'CHAR', 'CHAR', 'CHAR', 'CHAR', 'CHAR', 'CHAR', 'CHAR',
                  'CHAR', 'SPACE', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'COMMA', 'CHAR', 'OPEN_BRACKET', 'INT',
                  'CLOSE_BRACKET', 'SEMI_COLON', 'CHAR', 'CHAR', 'CHAR',
                  'CHAR', 'CHAR', 'CHAR', 'CHAR', 'SPACE','CHAR', 'ASSIGN_TO',
                  'SPACE', 'CHAR', 'SEMI_COLON']
if __name__ == '__main__':
    unittest.main()
