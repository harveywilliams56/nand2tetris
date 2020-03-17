// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// Make sure result starts with value 0 
  @R2
    M=0


//Check for edge cases 
  @R0
    D=M
  @End
    D;JEQ
  @R1
    D=M
  @End
    D;JEQ

  
// Init loop counter (n)
  @R1
    D=M
  @n
    M=D


//Main Loop
(Loop)
  @R0
    D=M
  @R2
    M=D+M

  @n
    M=M-1
    D=M
  @End
    D;JEQ
  @Loop
    0;JMP


(End)
  @End
    0;JMP

// Note to self:
// Could use bit-shifting - for every 1 at position n in the multiplier
// ...add the n-bit-shifted number to the total.
// This woudle save (2^n - 1) additions for every n!
// NB: Bit-shifting is how humans carry out decimal multiplication
//
// Note to anyone else:
// I have not done this in the first revision as this excersise is
// ...about learning to use the HACK assembly language

