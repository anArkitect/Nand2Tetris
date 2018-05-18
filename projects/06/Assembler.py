import Parser, Code, SymbolTable, sys

class Assembler(object):
    def __init__(self):
        self.symbols = SymbolTable.SymbolTable()
        # variable starts from 16
        self.var_addr = 16

    def pass0(self, file):
        parser = Parser.Parser(file)
        cur_pc = 0
        while parser.has_more_commands():
            parser.advance()
            cmd = parser.get_cmd_type()
            if cmd == parser.A_COMMAND or cmd == parser.C_COMMAND:
                cur_pc += 1
            elif cmd == parser.L_COMMAND:
                self.symbols.add_entry(parser.get_symbol(), cur_pc)

    def pass1(self, infile, outfile):
        parser = Parser.Parser(infile)
        outf = open(outfile, 'w')
        code = Code.Code()

        while parser.has_more_commands():
            parser.advance()
            cmd = parser.get_cmd_type()
            if cmd == parser.A_COMMAND:
                outf.write(code.gen_a_bits(self._get_address(parser.get_symbol()))+'\n')
            elif cmd == parser.C_COMMAND:
                outf.write(code.gen_c_bits(parser.get_dest(), parser.get_comp(), parser.get_jmp())+'\n')  
        outf.close()

    def _get_address(self, symbol):
        if symbol.isdigit():
            return symbol
        else:
            if not self.symbols.contains(symbol):
                self.symbols.add_entry(symbol, self.var_addr)
                self.var_addr += 1
            return self.symbols.get_address(symbol)

    def assemble(self, file):
        self.pass0(file)
        self.pass1(file, self._make_outfile(file))

    def _make_outfile(self, infile):
        if infile.endswith('.asm'):
            return infile.replace('.asm', '.hack')
        else:
            print("Only assembly files are supported.")
            exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage: Assembler file.asm")
    else:
        infile = sys.argv[1]

    asm = Assembler()
    asm.assemble(infile)


main()
