import Lex

class Parser(object):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def test(self):
        print("cmd type: " + str(self._cmd_type))
        print("symbol:   " + str(self._symbol))
        print("dest:     " + str(self._dest))
        print("comp:     " + str(self._comp))
        print("jump:     " + str(self._jmp))

    def __init__(self, file):
        self.lex = Lex.Lex(file)
        self._init_cmd_info()

    def _init_cmd_info(self):
        self._cmd_type = -1
        self._symbol = ''
        self._dest = ''
        self._comp = ''
        self._jmp = ''

    def has_more_commands(self):
        return self.lex.has_more_commands()

    def advance(self):
        self._init_cmd_info()

        self.lex.get_next_command()
        tok_t, val = self.lex.cur_token

        if tok_t == Lex.OP and val == '@':
            self._a_command()
        elif tok_t == Lex.OP and val == '(':
            self._l_command()
        else:
            self._c_command(tok_t, val)


    def _a_command(self):
        self._cmd_type = Parser.A_COMMAND
        tok_t, self._symbol = self.lex.get_next_token()

    def _l_command(self):
        self._cmd_type = Parser.L_COMMAND
        tok_t, self._symbol = self.lex.get_next_token()
    
    # dest=comp;jump
    # dest=comp         omitting jump
    # comp;jump         omitting dest
    # comp              omitting dest and jump
    def _c_command(self, tok1, val1):
        self._cmd_type = Parser.C_COMMAND
        comp_tok, comp_val = self._get_dest(tok1, val1)
        self._get_comp(comp_tok, comp_val)
        self._get_jump()

    def _get_dest(self, tok1, val1):
        tok2, val2 = self.lex.peek_next_token()
        if tok2 == Lex.OP and val2 == '=':
            self._dest = val1
            self.lex.get_next_token()
            comp_tok, comp_val = self.lex.get_next_token()
        else:
            comp_tok, comp_val = tok1, val1
        return (comp_tok, comp_val)

    #----------------------------------
    # a = 0             | a = 1
    #----------------------------------
    # 0 1 -1            |
    # D A !D !A -D -A   | M !M
    # D+1 A+1 D-1 A-1   | M+1 M-1
    # D+A D-A A-D       | D+M D-M M-D
    # D&A D|A           | D&M D|M 
    #----------------------------------
    # case 1:           | NUM
    # case 2:           | SYM
    # case 3:           | OP + SYM
    # case 4:           | SYM + OP + SYM(NUM)
    def _get_comp(self, tok_t, val):
        if tok_t == Lex.OP and (val == '!' or val == '-'):
            tok_t2, val2 = self.lex.get_next_token()
            self._comp = val + val2
            
        elif tok_t == Lex.NUM or tok_t == Lex.SYM:
            tok_t2, val2 = self.lex.peek_next_token()
            if val2 == ';':
                self._comp = val
            elif tok_t2 == Lex.OP:
                tok_t2, val2 = self.lex.get_next_token()
                tok_t3, val3 = self.lex.get_next_token()
                self._comp = val + val2 + val3
            else:
                self._comp = val
    
    def _get_jump(self):
        tok_t, val = self.lex.get_next_token()
        if val == ';':
            tok_t2, val2 = self.lex.get_next_token()
            self._jmp = val2
        else:
            pass

    def get_cmd_type(self):
        return self._cmd_type

    def get_symbol(self):
        return self._symbol

    def get_dest(self):
        return self._dest

    def get_comp(self):
        return self._comp

    def get_jmp(self):
        return self._jmp


# txt_to_test = '''
# // This file is part of www.nand2tetris.org
# // and the book "The Elements of Computing Systems"
# // by Nisan and Schocken, MIT Press.
# // File name: projects/06/max/Max.asm

# // Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])

#    @R0
#    D=M              // D = first number
#    @R1
#    D=D-M            // D = first number - second number
#    @OUTPUT_FIRST
#    D;JGT            // if D>0 (first is greater) goto output_first
#    @R1
#    D=M              // D = second number
#    @OUTPUT_D
#    0;JMP            // goto output_d
# (OUTPUT_FIRST)
#    @R0             
#    D=M              // D = first number
# (OUTPUT_D)
#    @R2
#    M=D              // M[2] = D (greatest number)
# (INFINITE_LOOP)
#    @INFINITE_LOOP
#    0;JMP            // infinite loop
# '''

# parser = Parser(txt_to_test)
# while parser.has_more_commands():
#     parser.advance()
#     parser.test()
#     print('---------------------------------')