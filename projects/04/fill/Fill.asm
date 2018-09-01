// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@i
M = 0
@current
M = 0

(IDLE)
@KBD
D = M
@CLEAR
D; JEQ
@FILL
D; JGT
@IDLE
0; JMP

(CLEAR)
@color
M = 0
@LOOP
0; JMP

(FILL)
@color
M = -1
@LOOP
0; JMP

(LOOP)
@i
D = M
@8192
D = D - A
@END
D; JGE

@SCREEN
D = A
@i
D = D + M

@current // set the current register.
M = D
@color
D = M
@current
A = M
M = D

@i
M = M + 1
@LOOP
0; JMP // restart the loop.

(END)
@i
M = 0 // Reset the index, and then start the process all over again.
@IDLE
0; JMP