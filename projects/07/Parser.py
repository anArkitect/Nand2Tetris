
import re
import sys



class Parser(object):

    C_ARITHMETIC = 0
    C_PUSH       = 1
    C_POP        = 2

    arithmetics = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']
    _cmd_type = -1

    # store the cotent of .vm file
    _lines = []
    def __init__(self, input_file):
        file_name = input_file
        if not file_name.endswith('.vm'):
            print('Only .vm files are supported')
            exit(1)
        with open(file_name, 'r') as new_file:
            self._lines = new_file.read().split('\n')
            #print(self._lines)


    def has_more_commands(self):
        return self._lines != []

    def advance(self):
        if self.has_more_commands():
            new_command = self._remove_comment(self._lines.pop(0))
            if new_command == '':
                return ''
            else:
                tokens = new_command.split(' ')
                if tokens[0] in self.arithmetics:
                    self._cmd_type = self.C_ARITHMETIC
                    return tokens
                elif tokens[0] == 'push':
                    self._cmd_type = self.C_PUSH
                    return tokens
                elif tokens[1] == 'pop':
                    self._cmd_type = self.C_POP
                    return tokens
        else:
            print("There is no more commands in .vm file, ERROR #1")
            exit(1)

    def get_command_type(self):
        return self._cmd_type

    def _remove_comment(self, line):
        _comment_pattern_1 = re.compile(r'/\*.*?\*/')
        _comment_pattern_2 = re.compile(r'//.*')
        _new_line = _comment_pattern_2.sub('', _comment_pattern_1.sub('', line))
        return _new_line

    def test(self):
        while(self.has_more_commands):
            val = self.advance()
            if val != '':
                print(self.get_command_type())
                print(val)