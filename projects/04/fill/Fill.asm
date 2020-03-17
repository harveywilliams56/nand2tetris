//  Set endpoint (finalAddr) for loop filling screen
  @SCREEN
    D=A
  @finalAddr
    M=D
  @8191
    D=A
  @finalAddr
    M=D+M


//Init with state: 0 (white)
  @state
    M=0


(Main)
  @KBD
    D=M
  @Keydepressed
    D;JNE
  @Notdepressed
    D;JEQ


(Keydepressed)
  @state
    D=M
  @Main
    D+1;JEQ  //Go back to Main if no change necessary

  @state
    M=-1
  @Draw
    0;JMP


(Notdepressed)
  @state
    D=M
  @Main
    D;JEQ   // Go back to Main if no change necessary

  @state
    M=0
  @Draw
    0;JMP
    

(Draw)
// Init addr
  @SCREEN
    D=A
  @addr
    M=D

(Drawloop)
// Write state to addr
  @state
    D=M
  @addr
  A=M
    M=D

// Go back to main if addr == finalAddr
  @finalAddr
    D=M
  @addr
    D=D-M
  @Main
    D;JEQ

// Else, iterate Drawloop
  @addr
    M=M+1
  @Drawloop
    0;JMP
