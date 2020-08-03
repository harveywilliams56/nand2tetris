#!/usr/bin/env python3
import sys
import re
from typing import NamedTuple

# Conscious decision not to implement detailed error reporting; majority of use should be on compiled code.
#   Language and documentation is simple enough that line-number should be sufficiently granular

# TODO Implement line-number error reporting

# Hash tables are an efficient way of translating - would be neat to code a helper tool that could
#   pre-compile these

# Pneumonic to binary conversion tables:
dest_dict = {"null":"000",
             "A":"100",
             "M":"001",
             "D":"010",
             "AD":"110",
             "MD":"011",
             "AM":"101",
             "AMD":"111"}

comp_dict = {"0":"0101010",
             "1":"0111111",
             "-1":"0111010",
             "D":"0001100",
             "A":"0110000",
             "M":"1110000",
             "!D":"0001101",
             "!A":"0110001",
             "!M":"1110001",
             "-D":"0001111",
             "-A":"0110011",
             "-M":"1110011",
             "D+1":"0011111",
             "A+1":"0110111",
             "M+1":"1110111",
             "D-1":"0001110",
             "A-1":"0110010",
             "M-1":"1110010",
             "D+A":"0000010",
             "A+D":"0000010",
             "D+M":"1000010",
             "M+D":"1000010",
             "D-A":"0010011",
             "D-M":"1010011",
             "A-D":"0000111",
             "M-D":"1000111",
             "D&A":"0000000",
             "A&D":"0000000",
             "D&M":"1000000",
             "M&D":"1000000",
             "D|A":"0010101",
             "A|D":"0010101",
             "D|M":"1010101",
             "M|D":"1010101"}

jump_dict = {"null":"000",
             "JGT":"001",
             "JEQ":"010",
             "JGE":"011",
             "JLT":"100",
             "JNE":"101",
             "JLE":"110",
             "JMP":"111"}

# C-like structs
class A_Instruction(NamedTuple):
    address: str

class C_Instruction(NamedTuple):
    dest: str
    comp: str
    jump: str


def translate_a_instruction(A_Instruction):
    return format(int(A_Instruction.address), '016b')

def translate_c_instruction(C_Instruction):
    return "111" + comp_dict[C_Instruction.comp] + dest_dict[C_Instruction.dest] + jump_dict[C_Instruction.jump]

def translate_null_instruction(null_str):
    return ''


def parse_a_instruction(cleaned_line):
    # There should be some rules about valid adresses
    return A_Instruction(address=cleaned_line[1:])

def parse_c_instruction(cleaned_line):
    # Needs policing to ensure assumptions based on valid instruction are usable
    check_for_dest = cleaned_line.split("=")

    if len(check_for_dest) == 2:  # Dest has been specified in instruction
        check_for_jump = check_for_dest[1].split(";")
        if len(check_for_jump) == 2:  # Jump has also been specified in instruction
            return C_Instruction(dest=check_for_dest[0], comp=check_for_jump[0], jump=check_for_jump[1])
        # Jump has not been specified in instruction
        return C_Instruction(dest=check_for_dest[0], comp=check_for_jump[0], jump='null')

    if len(check_for_dest) == 1:  # Dest has not been specified in instruction -> jump must be
        must_be_jump = check_for_dest[0].split(";")
        return C_Instruction(dest='null', comp=must_be_jump[0], jump=must_be_jump[1])



def parse_line(line):
    commentless_line = line.split("/", 1)[0]
    cleaned_line = re.sub(r'[\r\n\t]', '', commentless_line)

    if cleaned_line == '':
        return ('', translate_null_instruction)
    if cleaned_line[0] == '@':
        return (parse_a_instruction(cleaned_line), translate_a_instruction)
    else:
        return (parse_c_instruction(cleaned_line), translate_c_instruction)
            


if __name__ == "__main__":
    # Assuming that a .asm file has been given
    # TODO: create --help option and force asm extension
    infile_name = sys.argv[1]
    outfile_name = sys.argv[1][0:-3] + "hack"
    
    #TODO allow user to optionally increase buffer size
    with open(infile_name, 'r') as assembly_program:
        with open(outfile_name, 'w') as binfile:
            # Label checking should go here
            for line in assembly_program:
                (instruction, translator) = parse_line(line)
                binary = translator(instruction) # NB: "binary" is a string representation of binary code
                if binary != '':  # Better to be explicit than bool-y
                        binfile.write(binary + "\n")
