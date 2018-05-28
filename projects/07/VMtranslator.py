
import Parser, CodeWriter
import sys

def main():
    input_file = sys.argv[1]
    parser = Parser.Parser(input_file)
    output_file = input_file.replace('.vm', '.asm')
    code_writer = CodeWriter.CodeWriter(output_file)
    
    ###############
    #parser.output()
    ###############
    
    while parser.has_more_commands():
        tokens = parser.advance()
        if tokens == '':
            continue
        elif tokens[0] in parser.arithmetics:
            #print(tokens)
            code_writer.write_arithmetic(tokens)
        elif tokens[0] == 'push' or tokens[0] == 'pop':
            code_writer.write_push_pop(tokens)
    code_writer.close()


main()