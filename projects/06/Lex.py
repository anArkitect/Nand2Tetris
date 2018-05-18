# Test Checked

import re

NUM     = 1     # number e.g. '123'
SYM     = 2     # symbol e.g. 'LOOP'
OP      = 3     # = ; ( ) @ + - & | !
ERROR   = 4     # error in file

# Lexer is very simple.  Almost no error checking! - Assumes input will be program-generated.
# Detects numbers, symbols, and operators.
# Reads the whole .asm program into memory and uses regular expressions to match lexical tokens.

class Lex(object):
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self._lines = file.read()
        #self._lines = file_name
        self._tokens = self._tokenize_lines(self._lines.split('\n'))
        self.cur_command = []
        self.cur_token = (ERROR, 0)

    def has_more_commands(self):
        return self._tokens != []

    def get_next_command(self):
        self.cur_command = self._tokens.pop(0)
        self.get_next_token()
        return self.cur_command

    def has_next_token(self):
        return self.cur_command != []

    def get_next_token(self):
        if self.has_next_token():
            self.cur_token = self.cur_command.pop(0)
        else:
            self.cur_token = (ERROR, 0)
        return self.cur_token

    def peek_next_token(self):
        if self.has_next_token():
            return self.cur_command[0]
        else:
            return (ERROR, 0)

    def _tokenize_a_line(self, line):
        return [self._token(word) for word in self._split_a_line(self._remove_comment(line))]

    #! the starting and ending line is []
    def _tokenize_lines(self, lines):
        return [instruction for instruction in [self._tokenize_a_line(line) for line in lines] if instruction != []]

    def _is_num(self, word):
        return re.match(self._num_re, word)

    def _is_sym(self, word):
        return re.match(self._sym_re, word)
    
    def _is_op(self, word):
        return re.match(self._op_re, word)

    def _token(self, word):
        if self._is_num(word):
            return (NUM, word)
        elif self._is_sym(word):
            return (SYM, word)
        elif self._is_op(word):
            return (OP, word)
        else:
            return (ERROR, word)

    ## step 3: use reg
    def _split_a_line(self, line):
        return self._word.findall(line)

    ## step 2: remove comments
    def _remove_comment(self, line):
        _comment = re.compile(r'//.*$')
        return _comment.sub('', line)

    # case 1:
    #   if it starts with a number, then it must be a number 
    # case 2:
    #   symbol must start with a non-digit character
    # case 3:
    #   number & symbol are separated by operators
    _num_re = r'\d+'
    _sym_re = r'[\w.$_]+'
    _op_re  = r'[()@\-=;&|!]'
    _word = re.compile(_num_re + r'|' + _sym_re + r'|' + _op_re)

    