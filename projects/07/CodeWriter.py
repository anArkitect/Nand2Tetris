
# R15: FOR COPY

class CodeWriter(object):

    _label_num = 0

    def __init__(self, output_file):
        self._new_file = open(output_file, 'w')

    def set_file_name(self):
        pass

    def write_arithmetic(self, command):
        if command[0] == 'add':     self._add()
        elif command[0] == 'sub':   self._sub()
        elif command[0] == 'neg':   self._neg()
        elif command[0] == 'eq':    self._eq()
        elif command[0] == 'lt':    self._lt()
        elif command[0] == 'gt':    self._gt()
        elif command[0] == 'and':   self._and()
        elif command[0] == 'or':    self._or()
        elif command[0] == 'not':   self._not()

    # Segments: constant + local + argument + this + that + temp
    def write_push_pop(self, tokens):
        if tokens[0] == 'push':
            if tokens[1] == 'constant':         self._push_constant(tokens[2])
            elif tokens[1] == 'local':          self._push_segment('LCL', tokens[2])
            elif tokens[1] == 'argument':       self._push_segment('ARG', tokens[2])
            elif tokens[1] == 'this':           self._push_segment('THIS', tokens[2])
            elif tokens[1] == 'that':           self._push_segment('THAT', tokens[2])
            elif tokens[1] == 'temp':           self._push_segment('temp', tokens[2])
            elif tokens[1] == 'pointer':        self._push_pointer(tokens[2])
        elif tokens[0] == 'pop':
            if tokens[1] == 'local':            self._pop_segment('LCL', tokens[2])
            elif tokens[1] == 'argument':       self._pop_segment('ARG', tokens[2])
            elif tokens[1] == 'this':           self._pop_segment('THIS', tokens[2])
            elif tokens[1] == 'that':           self._pop_segment('THAT', tokens[2])
            elif tokens[1] == 'temp':           self._pop_segment('temp', tokens[2])
            elif tokens[1] == 'pointer':        self._pop_pointer(tokens[2])


    def _push_pointer(self, value):
        if value == '0':
            new_str =   '    @3\n'
        elif value == '1':
            new_str =   '    @4\n'
        new_str +=      '    D=M\n'             +\
                        '    @SP\n'             +\
                        '    A=M\n'             +\
                        '    M=D\n'             +\
                        '    @SP\n'             +\
                        '    M=M+1\n'
        self._new_file.write(new_str)

    def _pop_pointer(self, value):
        if value == '0':
            get_ptr =   '    @3\n'
        elif value == '1':
            get_ptr =   '    @4\n'
        new_str =       '    @SP\n'             +\
                        '    AM=M-1\n'          +\
                        '    D=M\n'             +\
                        get_ptr                 +\
                        '    M=D\n'             
        self._new_file.write(new_str)

    def _push_constant(self, value):
        self._new_file.write('//push constant ' + value + '\n')
        new_str =   '    @' + value + '\n'      +\
                    '    D=A\n'                 +\
                    '    @SP\n'                 +\
                    '    A=M\n'                 +\
                    '    M=D\n'                 +\
                    '    @SP\n'                 +\
                    '    M=M+1\n'                   
        self._new_file.write(new_str)


    def _push_segment(self, segment, value):
        self._new_file.write('//push ' + segment + ' ' + value + '\n')
        if segment == 'temp':       
            new_str = '    @5\n' + '    D=A\n'
        else:                       
            new_str = '    @' + segment + '\n' + '    D=M\n'
        new_str +=  '    @' + value + '\n'      +\
                    '    A=A+D\n'               +\
                    '    D=M\n'                 +\
                    '    @SP\n'                 +\
                    '    A=M\n'                 +\
                    '    M=D\n'                 +\
                    '    @SP\n'                 +\
                    '    M=M+1\n'
        self._new_file.write(new_str)

    #TODO
    def _pop_segment(self, segment, value):
        self._new_file.write('//pop ' + segment + ' ' + value + '\n')
        if segment == 'temp':       
            pt_seg = '    @5\n' + '    D=A\n'
        else:
            pt_seg = '    @' + segment + '\n' + '    D=M\n'
        new_str =   '    @SP\n'                 +\
                    '    AM=M-1\n'              +\
                    '    D=M\n'                 +\
                    '    @R15\n'                +\
                    '    M=D\n'                 +\
                    pt_seg                      +\
                    '    @' + value + '\n'      +\
                    '    D=A+D\n'               +\
                    '    @R14\n'                +\
                    '    M=D\n'                 +\
                    '    @R15\n'                +\
                    '    D=M\n'                 +\
                    '    @R14\n'                +\
                    '    A=M\n'                 +\
                    '    M=D\n'
        self._new_file.write(new_str)

    def close(self):
        self._new_file.close()

    def _add(self):
        new_str =   '//add\n'                   +\
                    '    @SP\n'                 +\
                    '    AM=M-1\n'              +\
                    '    D=M\n'                 +\
                    '    A=A-1\n'               +\
                    '    M=M+D\n'               
        self._new_file.write(new_str)
    
    def _sub(self):
        new_str =   '//sub\n'                   +\
                    '    @SP\n'                 +\
                    '    AM=M-1\n'               +\
                    '    D=M\n'                 +\
                    '    A=A-1\n'               +\
                    '    M=M-D\n'               
        self._new_file.write(new_str)

    def _neg(self):
        new_str =   '//neg\n'                   +\
                    '    @SP\n'                 +\
                    '    A=M-1\n'               +\
                    '    M=-M\n'                            
        self._new_file.write(new_str)

    def _eq(self):
        self._compare('JEQ')

    def _gt(self):
        self._compare('JGT')

    def _lt(self):
        self._compare('JLT')

    def _compare(self, condition):
        new_label = self._create_new_label()

        # Assume the result is True
        # if it is the case, then jump to label 
        # else result is assigned with false
        new_str =   '//' + new_label + '\n'     +\
                    '    @SP\n'                 +\
                    '    AM=M-1\n'              +\
                    '    D=M\n'                 +\
                    '    A=A-1\n'               +\
                    '    D=M-D\n'               +\
                    '    M=-1\n'                +\
                    self._a_command(new_label)  +\
                    '    D;' + condition + '\n' +\
                    '    @SP\n'                 +\
                    '    A=M-1\n'               +\
                    '    M=0\n'                 +\
                    self._l_command(new_label)
        self._new_file.write(new_str)

    def _and(self):
        self._logic('&')

    def _or(self):
        self._logic('|')
    
    def _not(self):
        new_str =   '//not\n'                   +\
                    '    @SP\n'                 +\
                    '    A=M-1\n'               +\
                    '    M=!M\n'
        self._new_file.write(new_str)
        
    def _logic(self, logic):
        new_str =   '//' + logic + '\n'         +\
                    '    @SP\n'                 +\
                    '    AM=M-1\n'               +\
                    '    D=M\n'                 +\
                    '    A=A-1\n'               +\
                    '    M=M' + logic +'D\n'   
        self._new_file.write(new_str)

    # operation components
    def _dec_sp(self):
        self._a_command('SP')
        self._c_command('M', 'M-1')

    def _inc_sp(self):
        self._a_command('SP')
        self._c_command('M', 'M+1')


    def _a_command(self, addr):
        return '    @' + addr + '\n'

    def _c_command(self, dest, comp, jump=None):
        self._new_file.write(' ' * 4)
        if dest != None:
            self._new_file.write(dest + '=')
        self._new_file.write(comp)
        if jump != None:
            self._new_file.write(';'+jump)
        self._new_file.write('\n')
    
    def _l_command(self, label):
        return '(' + label + ')\n'

    def _create_new_label(self):
        label = 'label' + str(self._label_num)
        self._label_num += 1
        return label