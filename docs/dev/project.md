# QEDA Project Plan

[TOC]



## Scope

QEDA is a command-line tool used to automate the design of linear optical quantum circuits. A user with limited circuit design knowledge will be able to design an optical quantum circuit using the OpenQASM standard. The idea is to limit the time and cost to design linear optical quantum circuits.

The software will consist of a number of inputs created as pcb and library files including the following:

1. User Created OpenQASM design file
2. PCB configuration file - conf/pcb.conf
3. Library configuration file - conf/libs.conf
4. PCB layouts -  lib/Quantum.pretty
5. Schematic footprints - lib/Quantum.lib

Outputs Include:

1. User created kicad schematic
2. User created kicad PCB layout
3. CLI debugging output

## Major Software Functions

### Process & Control Functions
* CLI Interface - The interface is the subsystem the user interacts with. It creates a project folder for all project files to be stored in. It gathers all necessary data from the user and configuration files.
* QEDA Manager - This subsystem is the main code generation function of the system. The manager creates .kicad_pcb and .sch files for the quantum circuits.
### User Interface Processing
* CLI
### Input Processing
* conf/components.conf - QEDA utilizes a components configuration file to allow modularity and implementation of new components.
* conf/pcb.conf - QEDA utilizes a pcb configuration file to alter the generated PCB settings

### Management

* qeda.py - Creates a new QEDA manager object to handle circuit generation.

### Compilation

* parser.py - parses the OpenQASM input provided by the user.
* qast.py - Abtract syntax tree for the parser, generates qcode dictionary

### Libraries/Modules

* lib/libs - kicad PCB footprints pulled in by pcb.py during layout generation
* lib/modules - Kicad schematic libraries pulled in by schema.py during schematic generation.

### Output Processing

* pcb.py generates PCB layout files.
* schema.py generates schematic files.

## Performance/Behavior Issues

QEDA is designed to be compatible with Linux Mint 18+, while the software should run fine without modification on other Debian based distributions and most linux operating systems, other distros and earlier versions will not be supported.

QEDA also requires Python3.6+ and Kicad5+, earlier versions of these software will not be supported.

QEDA also requires the python packages numpy and pykicad.

## Management and Technical Constraints

QEDA has a delivery date of 12/31/2020.

Spooky Manufacturing will be using the Rapid Prototyping model during design and implementation.

## Project Estimates

A project estimate was calculated using function point analysis.

#### Estimation Techniques Applied and Results

A reference Function Point metric was calculated using typical complexity averages.

The following is a breakdown of the numbers used in estimating the Function Point for QEDA:

| Function Units | Simple | Avg  | Complex |
| -------------- | ------ | ---- | ------- |
| EI             | 3      | 4    | 6       |
| EO             | 4      | 5    | 7       |
| EQ             | 3      | 4    | 6       |
| ILF            | 7      | 10   | 15      |
| EIF            | 5      | 7    | 10      |


Command Line Interface Estimates

| Interface                     | Simple | Average | Complex | UFP  |
| ----------------------------- | ------ | ------- | ------- | ---- |
| Number of User Inputs         | 2      | 1       |         | 10   |
| Number of User Outputs        |        | 1       | 3       | 34   |
| Number of User Inquiries      | 2      | 1       | 1       | 16   |
| Number of Files               | 2      | 3       | 4       | 104  |
| Number of External Interfaces |        |         | 1       | 10   |

Function Point:  293.18

| Manager                       | Simple | Average | Complex | UFP  |
| ----------------------------- | ------ | ------- | ------- | ---- |
| Number of User Inputs         |        | 5       | 1       | 26   |
| Number of User Outputs        | 1      | 1       | 2       | 23   |
| Number of User Inquiries      |        |         |         | 0    |
| Number of Files               | 2      | 3       | 4       | 104  |
| Number of External Interfaces | 0      | 0       | 2       | 20   |

Function Point: 185.11

#### Time and Code Estimates

Using the above table and industry average FP productivity per month of 28.06 we can  calculate a duration estimate for QEDA:

Interface: 293.18
Manager: 185.11
Total Function Points:  478.29
Estimated person months: 17.04



LOC = FP*30
Estimated lines of code: 14,379

## Project Resources

While a complete team would contain all of the following personnel, Spooky Manufacturing has 1 member who will perform multiple jobs.

*Required Staff*

* Lead Python Programmer
* Assistant Python Programmer
* Quantum Engineer
* Documentation
* Manual Designer
* Beta Testers

No special development systems are required for QEDA. Spooky Manufacturing will be using PCs and commonly available software.

*Required Hardware*

* 1 Development System
  - Samsung Chromebook
  - 2GB RAM
  - 1TB External HDD

*Required Software*

* Linux Mint 19
* Python3.6
* Kicad
* PyKicad
* NumPy

## Risk Management

### Project Risks

Major risks we have determined for this software are as follows:

* Equipment failure
* Late delivery of software
* Technology will not meet expectations
* Changes in requirements
* Deviation from software engineering standards
* Less reuse than planned
* Poor commenting of source code

## Project Schedule

Spooky Manufacturing will be using the Rapid Prototyping model during design and implementation.

*Framework Activities*

* Planning/Design
* Programming
* Testing
* Evaluation

*Task Set*

* Requirements Specification
* Interface Construction
* Manager Construction
* Compiler Construction
* Testing

### List of Deliverables

*Documentation*

* System Requirements Specification
* Software Requirements Specification
* Design Document
* Project Plan

*Code*

* CLI Prototypes
* QEDA Processing Prototypes
* Library Prototypes
* Modules Prototypes
* 3D Component Prototypes
* Complete CLI
* Complete QEDA
* Complete Libraries
* Complete Modules
* Complete 3D Components
* Integrated System
* Complete Product

## Project Timeline

blah