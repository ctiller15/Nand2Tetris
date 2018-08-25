// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@i
M = 1
@prod
M = 0
@R2
M = 0

(LOOP)
@i
D = M
@R0
D = D - M // Checking current incrementor.

@SET
D; JGT // If D is > 0, go to SET value.
@R1
D = M // Setting D to the first register.
@prod
M = D + M
@i
M = M + 1 // Incrementing the index.
@LOOP
0; JMP // Restarts the loop.

(SET)
@prod
D = M
@R2
M = D

(END)
@END
0; JMP
