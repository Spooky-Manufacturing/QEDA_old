// Blah //
OPENQASM 2.0;
X(1);
X(2);
CX 1,2;
CX 2,1;
MEASURE 1 -> 0;
MEASURE 2 -> 1;
