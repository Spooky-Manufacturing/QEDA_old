#!/usr/bin/python3
import getopt
import sys
from qeda.parser import Parser
from qeda.lexer import Lexer

goal_text_input = """// Quantum Experience (QE) Standard Header// file: qelib1.inc// --- QE Hardware primitives ---// 3-parameter 2-pulse single qubit gategate u3(theta,phi,lambda) q { U(theta,phi,lambda) q; }// 2-parameter 1-pulse single qubit gategate u2(phi,lambda) q { U(pi/2,phi,lambda) q; }// 1-parameter 0-pulse single qubit gategate u1(lambda) q { U(0,0,lambda) q; }// controlled-NOT gate cx c,t { CX c,t; }// idle gate (identity)gate id a { U(0,0,0) a; }// --- QE Standard Gates ---// Pauli gate: bit-flipgate x a { u3(pi,0,pi) a; }// Pauli gate: bit and phase flipgate y a { u3(pi,pi/2,pi/2) a; }// Pauli gate: phase flipgate z a { u1(pi) a; }// Clifford gate: Hadamardgate h a { u2(0,pi) a; }// Clifford gate: sqrt(Z) phase gategate s a { u1(pi/2) a; }// Clifford gate: conjugate of sqrt(Z)gate sdg a { u1(-pi/2) a; }// C3 gate: sqrt(S) phase gategate t a { u1(pi/4) a; }// C3 gate: conjugate of sqrt(S)gate tdg a { u1(-pi/4) a; }// --- Standard rotations ---// Rotation around X-axisgate rx(theta) a { u3(theta,-pi/2,pi/2) a; }// rotation around Y-axisgate ry(theta) a { u3(theta,0,0) a; }// rotation around Z axisgate rz(phi) a { u1(phi) a; }// --- QE Standard User-Defined Gates  ---// controlled-Phasegate cz a,b { h b; cx a,b; h b; }// controlled-Ygate cy a,b { sdg b; cx a,b; s b; }// controlled-Hgate ch a,b {h b; sdg b;cx a,b;h b; t b;cx a,b;t b; h b; s b; x b; s a;}11 // C3 gate: Toffoligate ccx a,b,c{h c;cx b,c; tdg c;cx a,c; t c;cx b,c; tdg c;cx a,c; t b; t c; h c;cx a,b; t a; tdg b;cx a,b;}// controlled rz rotationgate crz(lambda) a,b{u1(lambda/2) b;cx a,b;u1(-lambda/2) b;cx a,b;}// controlled phase rotationgate cu1(lambda) a,b{u1(lambda/2) a;cx a,b;u1(-lambda/2) b;cx a,b;u1(lambda/2) b;}// controlled-Ugate cu3(theta,phi,lambda) c, t{// implements controlled-U(theta,phi,lambda) with  target t and control cu1((lambda-phi)/2) t;cx c,t;u3(-theta/2,0,-(phi+lambda)/2) t;cx c,t;u3(theta/2,phi,0) t;}3.2"""
text_input = """
// THHHHIS X CX CCNOT BLAH I  //
I(1);
OPENQASM 1
H(1);
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
#print([x for x in tokens])
pg = Parser()
pg.parse()
parser = pg.get_parser()
parser.parse(tokens).eval()


