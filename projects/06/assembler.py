# This is an assembler made for project 6 of the nand to tetris course.
import os
import sys
import re

print(sys.argv[1])
# Initializing all relevant dictionaries.
compAzero = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '110000',
    '!D': '001101',
    '!A': '110001',
    '-D': '001111',
    '-A': '110011',
    'D+1': '011111',
    'A+1': '110111',
    'D-1': '001110',
    'A-1': '110010',
    'D+A': '000010',
    'D-A': '010011',
    'A-D': '000111',
    'D&A': '000000',
    'D|A': '010101',
}

compAone = {
    'M': '110000',
    '!M': '110001',
    '-M': '110011',
    'M+1': '110111',
    'M-1': '110010',
    'D+M': '000010',
    'D-M': '010011',
    'M-D': '000111',
    'D&M': '000000',
    'D|M': '010101',
}

destMap = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}

jumpMap = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

fileName = sys.argv[1]
outfileName = f"{os.path.splitext(fileName)[0]}.hack"
print(fileName)
print(outfileName)

#Opening file.
f = open(fileName, 'r')

instructions = []

#Clearing out line comments and whitespace.
for line in f:
    if(line != "\n" and not(line.startswith('//'))):
        instructions.append(line.strip())

print(instructions)

# Parsing the individual sections for each instruction.

#First, identify if A instruction or C-instruction.

def HandleAInstruction(instruction):
    #print('A instruction')
    ainst = '0' + bin(int(instruction[1:]))[2:].zfill(15)
    return ainst

def HandleCInstruction(instruction):
    cdjinst = []
    comp = 'null'
    dest = 'null'
    jump = 'null'
    if('=' in instruction and ';' in instruction):
        cdjinst = re.split('= |; ', instruction)
        dest, comp, jump = cdjinst
    elif('=' in instruction):
        cdjinst = re.split('=', instruction)
        dest, comp = cdjinst
    elif(';' in instruction):
        cdjinst = re.split(';', instruction)
        comp, jump = cdjinst
    else:
        cdjinst = instruction
    return f'111{HandleCompInstruction(comp)}{destMap[dest]}{jumpMap[jump]}'

def HandleCompInstruction(instruction):
    if(instruction in compAzero.keys()):
        comp = '0' + compAzero[instruction]
    elif(instruction in compAone.keys()):
        comp = '1' + compAone[instruction]
    return comp

#Parser.
def Parser(instructions):
    parsed = []
    for instr in instructions:
        if(instr.startswith('@')):
            parsed.append(HandleAInstruction(instr))
        else:
            parsed.append(HandleCInstruction(instr))
    return parsed

parsedInstructions = Parser(instructions)
print(parsedInstructions)

f.close()

# Writing to file.
with open(outfileName, 'w') as g:
    for line in parsedInstructions:
        g.write(f"{line}\n")
#g = open(outfileName, 'w')
