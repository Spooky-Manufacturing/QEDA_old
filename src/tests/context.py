import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qeda.lexer import Lexer
from qeda.parser import Parser
from qeda import qast
