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


// Set endpoint (n) for loops filling the screen
  @8192
    D=A
  @n
    M=D


(White)
  @i
    M=0
(Wdrawloop)
  @SCREEN
    D=A
  @i
  A=D+M
    M=0

  @i
    M=M+1
    D=M

  @n
    D=M-D
  @Wdrawloop     
    D;JGT

(Wloop)
  @KBD
    D=M
  @Black
    D;JNE
  @Wloop
    0;JMP
    
  
(Black)
  @i
    M=0
(Bdrawloop)
  @SCREEN
    D=A
  @i
  A=D+M
    M=-1

  @i
    M=M+1
    D=M

  @n
    D=M-D
  @Bdrawloop     
    D;JGT

(Bloop)
  @KBD
    D=M
  @White
    D;JEQ
  @Bloop
    0;JMP


(End)
  @End
    0;JMP
