

class CodeWriter(object):
    def __init__(self, output_file):
        self._new_file = open(output_file, 'w')

    def set_file_name(self):
        pass

    def write_arithmetic(self, tokens):
        if tokens[0] == 'add':
            new_str = '''    @SP
    A=M-1
    D=M
    A=A-1
    M=D+M
    @SP
    M=M-1
    '''
            self._new_file.write(new_str)   

    def write_push_pop(self, tokens):
        if tokens[0] == 'push':
            if tokens[1] == 'constant':
                new_str = '    @' + tokens[2] + \
'''
    D=A
    @SP
    A=M
    M=D
    @SP
    M=M+1
'''
                self._new_file.write(new_str)
    
    def close(self):
        self._new_file.close()