OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

h q;
cx q, q[2];
cx q, q[1];

measure q -> c;
