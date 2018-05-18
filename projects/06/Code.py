# Test Checked

class Code(object):
    def __init__(self):
        pass

    def gen_a_bits(self, addr):
        return '0' + self._to_bits(addr).zfill(15)

    def gen_c_bits(self, dest, comp, jump):
       return '111' + self._comp(comp) + self._dest(dest) + self._jump(jump) 

    def _to_bits(self, addr):
        return bin(int(addr))[2:]

    def _dest(self, dest):
        dest_list = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
        return self._to_bits(dest_list.index(dest)).zfill(3)

    def _comp(self, comp):
        comp_dict = \
        { 
            '0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
            'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
            '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
            'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
            'D&A':'0000000','D|A':'0010101',
            '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx',   '':'xxxxxxx', 
            'M':'1110000',  '':'xxxxxxx',   '!M':'1110001', '':'xxxxxxx', 
            '-M':'1110011', '':'xxxxxxx',   'M+1':'1110111','':'xxxxxxx', 
            'M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111', 
            'D&M':'1000000', 'D|M':'1010101' 
        }
        return comp_dict[comp]

    def _jump(self, jump):
        jump_list = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']
        return self._to_bits(jump_list.index(jump)).zfill(3)