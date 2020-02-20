import importlib

from qeda.lexer import Lexer
from qeda.parser import Parser
from qeda.schema import SchemaBuilder
from qeda.pcb import PCBBuilder

class QEDAManager:
    """QEDA Manager Class
        The QEDA Manager class takes inputs from the CLI or other interfaces
        and generates the requested PCB and Schematic layouts.
        Parameters
        ----------
        infile : str
            location of the qasm file
        outfile : str
            location to store output files
        processors : int
            Number of processors to use (default 1)
        verbose : bool (default False)
            Toggles terminal debugging output
        make_pcb : bool (default True)
            Toggles whether to make a PCB layout
        make_schema : bool (default True)
            Toggles whether to make the schematic files.
        Attributes
        ----------
        """
    def __init__(self, infile, outfile=None, processors=1,
                 verbose=False, make_pcb=True, make_schema=True):
        self.infile = infile
        self.outfile = outfile
        self.processors = processors
        self.verbose = str(verbose).lower()
        self.make_pcb = make_pcb
        self.make_schema = make_schema
        # Setup up verbosity
        self.verbose_setup()
        
        # Initialization verification
        self.init_checks()

        # Call multiprocessor manager
        if processors > 1:
            self.mp_manager()
        else:
            # Call the main block
            self.main_block()

    def verbose_setup(self):
        global V
        V = getattr(importlib.import_module("qeda.verbose", self.verbose), self.verbose)
        V("Verbosity setup complete")

    def init_checks(self):
        if self.infile == None:
            raise Exception('Error: No input file specified')
        if self.outfile == None:
            self.outfile = self.infile + '.out'
            V("Outfile: {}".format(self.outfile))
        if self.make_pcb == self.make_schema == False:
            V("No work to be done.")
            sys.exit(0)

    def mp_manager(self):
        """The multiprocessor manager, spawns and delegates tasks if possible"""
        
        pass

    def main_block(self):
        """Completes the operations required."""
        try:
            lines = self.read_file()
            V("Lines", lines)
            tokens = self.call_lexer(lines)
            V("Tokens", tokens)
            qcode = self.call_parser(tokens)
            V("QCode", qcode)
            if self.make_pcb == True:
                self.call_pcb_maker(qcode)
            if self.make_schema == True:
                self.call_schema_maker(qcode)
            
        except Exception as e:
            V("An error occurred.")
            V(e)
            return 1, e

    def read_file(self):
        V("Opening {}".format(self.infile.split('/')[-1]))
        with open(self.infile, 'r') as f:
            lines = ''.join([x for x in f.readlines()])
        return lines

    def call_lexer(self, lines):
        lexer = Lexer().get_lexer()
        return lexer.lex(lines)

    def call_parser(self, tokens):
        page = Parser(self.verbose)
        page.parse()
        parser = page.get_parser()
        return parser.parse(tokens)#.eval()

    def call_pcb_maker(self, qcode):
        PCBBuilder(qcode, verbose=self.verbose)

    def call_schema_maker(self, qcode):
        SchemaBuilder(qcode)
