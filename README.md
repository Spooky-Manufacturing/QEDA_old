# QEDA
Quantum electronic design automation software for optical circuits

# Motivation
After spending 4 months designing by hand a single qubit optical computer, I realized we needed an easier way to design optical circuits and processors. Thus was the inspiration behind the creation of QEDA, a reverse-compiler of sorts that takes standard QASM code and generates circuit schematics and PCB layouts for rapid prototyping.

# Coding Style
Currently, winging it! We'll be looking to move towards proper PEP coding and documentation style though in the near future. Rewrites to bring the code back into proper style are welcome!

# Requirements
Kicad (Version 5.0+ preferred)
rply
pykicad
numpy

# Installation
You will need to install kicad on your own, we would like to release an automated script to help this process along though. You will also need to manually add in the footprints and libraries found in the src/lib and src/modules folders

# How To Use
QEDA uses standard QASM to design the circuits. Currently the software isn't entirely functional, more logic gates need to be implemented, and the AST needs to be finished before we can see real results. To get a glimpse of how the software will run when complete, run main.py

# Contribute
If you would like to contribute, it would be much appreciated! We need documentation on our Wiki, logic gates to be designed in kicad, and placement algorithms to be implemented. An IDE may be 
