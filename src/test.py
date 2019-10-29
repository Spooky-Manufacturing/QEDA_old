#!/usr/bin/python3
import getopt
import sys
from qeda.parser2 import Parser
from qeda.lexer import Lexer

def test():
    """Runs the test suite"""
    print('testing')

    import unittest
    from tests.lexer_tests import LexerTests
    from tests.qast_tests import QAST_Tests
    from tests.parser_tests import ParserTest

    unittest.main()
    sys.exit(0)

def qeda_help():
    """Returns the help information"""
    print("Help")

def build_pcb(parsed):
    """Builds the PCB from parsed data"""
    pass

def run(infile, outfile, processors, threads):
    """Runs QEDA from a file"""
    print('run:', infile, outfile, processors, threads)
    with open(infile, 'r') as f:
        lexer = Lexer().get_lexer()
        lines = ''.join([x for x in f.readlines()])
        tokens = lexer.lex(lines)
    page = Parser()
    page.parse()
    parser = page.get_parser()
    parser.parse(tokens)

def main(args=None):
    """The main routine"""
    processors = 0
    threads = 0
    unix_options = "hotpm:v"
    gnu_options = ["help", "output=", "test", "processors=",
                   "multithreaded", "verbose"]
    if args is None:
        args = sys.argv[1:]
        # help command
        if args[0] in ("h", "-h", "--help"):
            qeda_help()
            return 0
    try:
        arguments, vals = getopt.getopt(args[1:], unix_options, gnu_options)
        infile = args[0]
        outfile = args[0].split('.')[0]
        for current_arg, current_val in arguments:
            print(current_arg, current_val)
            if current_arg in ("v", "-v", "--verbose"):
                outfile = "verbose"
                print("enabling verbose mode")
            elif current_arg in ("-o", "--output"):
                # Must use --o file or --output=file
                outfile = current_val
            elif current_arg in ("t", "-t", "--test"):
                test()
            elif current_arg in ("p", "-p", "--processors"):
                print('p')
                # Need to implement multiprocessing
                raise NotImplementedError("Multiprocessing has not yet been implemented")
            elif current_arg in ("m", "-m", "--multithreaded"):
                print('m')
                raise NotImplementedError("Multithreading has not yet been implemented")
                # Need to implement multithreading
        run(infile, outfile, processors, threads)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
if __name__ == "__main__":
    main()
