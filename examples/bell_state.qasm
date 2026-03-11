OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[1];

h q;
cx q, q[2];

measure q -> c;
