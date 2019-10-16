# QEDA Documentation

This software is currently a work in progress, there is much work to be done including the writing of tests, verification of code, etc. while the program should run fine out of the box, there is no guarantee this will be the case.

## Contributing
If you would like to contribute to the QEDA source code, fork the repository and start hacking away!

### How It Works
The software is written in a similar way to a compiler, only rather than building a high level language into assembly it builds assembly language into a circuit diagram and PCB layout.

User input (e.g. a file) is read into memory, tokenized by lexer.py, parsed using parser.py which calls the abstract syntax tree qast.py. The abstract syntax tree will then return a list of objects to the parser which calls pcb.py and schema.py to build out the layout and schematic.

### What needs to be done?
We need to glue together these scripts into a single main.py file, a reformat of the structure and thorough documentation is also in order.


