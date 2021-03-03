import unittest

from tests.context import Lexer, Parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer().get_lexer()
        self.page = Parser()
        self.page.parse()
        self.parser = self.page.get_parser()

    def test_space(self):
        pass


if __name__ == '__main__':
    unittest.main()
