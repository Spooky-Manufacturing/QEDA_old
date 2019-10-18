//Repetition code syndrome measurement//
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
qreg a[2];
creg c[3];
creg syn[2];
gate syndrome d1,d2,d3,a1,a2{
cx d1,a1; cx d2,a1;
cx d2,a2; cx d3,a2;
}
X q[0];//Error//
barrier q;
syndrome q[0],q[1],q[2],a[0],a[1];
measure a -> syn;
if(syn==1) X q[0];
if(syn==2) X q[2];
if(syn==3) X q[1];
measure q -> c;
