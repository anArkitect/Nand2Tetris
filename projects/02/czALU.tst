// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/02/ALU.tst

load ALU.hdl,
output-file czALU.out,
compare-to czALU.cmp,
output-list x%B1.16.1 y%B1.16.1 zx%B1.1.1 nx%B1.1.1 zy%B1.1.1 
            ny%B1.1.1 f%B1.1.1 no%B1.1.1 out%B1.16.1 zr%B1.1.1
            ng%B1.1.1;

set x %B0000000000000001,  // x = 0
set y %B1111111111111111;  // y = -1


// Compute x + 1
set zx 0,
set nx 1,
set zy 1,
set ny 1,
set f  1,
set no 1,
eval,
output;
