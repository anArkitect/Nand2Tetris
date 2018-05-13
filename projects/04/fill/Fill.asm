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

// thought: by SCREEN & KBD
// black: M = -1
// white: M = 0


    // [para] status: 0 -- white / 1 -- black
    @oldstatus
    M = 0


(LOOP)
    @offset
    M = 0

    @KBD
    D = M

    @SETONE
    D; JGT

    @SETZERO
    0; JMP



(SETWHITE)
    @8192
    D = A

    @offset
    D = D - M

    @LOOP
    D; JEQ

    @offset
    D = M

    @SCREEN
    A = A + D
    M = 0

    @offset
    M = M + 1

    @SETWHITE
    0; JMP


(SETBLACK)
    @8192
    D = A 

    @offset
    D = D - M

    @LOOP
    D; JEQ

    @offset
    D = M

    @SCREEN
    A = A + D
    M = -1

    @offset
    M  = M + 1

    @SETBLACK
    0; JMP


(SETZERO)
    @newstatus
    M = 0
    D = M

    @oldstatus
    D = D - M
    
    // if both oldstatus & newstatus == 0, we do nothing
    @LOOP       
    D; JEQ

    // else we change oldstatus = 0, and set screen to be white
    @oldstatus
    M = 0

    @SETWHITE
    0; JMP


(SETONE)
    @newstatus
    M = 1
    D = M
    
    @oldstatus
    D = D - M

    @LOOP
    D; JEQ

    @oldstatus
    M = 1

    @SETBLACK
    0; JMP

