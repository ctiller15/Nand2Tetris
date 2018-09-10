# This is an assembler made for project 6 of the nand to tetris course.
import os
import sys
import re
import mapVars

fileName = sys.argv[1]
outfileName = f"{os.path.splitext(fileName)[0]}.hack"

#Opening file.
f = open(fileName, 'r')

instructions = []
labels = {}
RAMsymbols = mapVars.RAMsymbols

#Clearing out line comments and whitespace.
for line in f:
    templine = line
    firstCommentInd = templine.find('//')
    if(firstCommentInd >= 0):
        templine = templine[0:firstCommentInd]
    if(line != "\n" and not(line.startswith('//'))):
        templine = templine.strip()
        instructions.append(templine)

# Find all lines with symbols/labels.
def findLabels(instructions):
    for index, value in enumerate(instructions):
        #If it is a label, add it to the labels dict.
        if(value[0] == "("):
            labels[value[1:-1]] = index - len(labels)

def findRAMAddresses(instructions):
    for inst in instructions:
        if(inst[0] == "@"):
            if(not(inst[1].isalpha()) or (inst[1:] in labels) or (inst[1:] in mapVars.specialLabels)):
                pass
            elif(inst[1:] not in RAMsymbols):
                RAMsymbols[inst[1:]] = len(RAMsymbols)

def clearLabels(instructions):
    clearedLabels = list(filter(lambda inst : inst[0] != '(', instructions))
    return clearedLabels

#Converts an A instruction.
def HandleAInstruction(instruction):
    ainst = ""
    if(instruction[1].isalpha()):
        if(instruction[1:] in mapVars.specialLabels):
            index = mapVars.specialLabels[instruction[1:]]
            ainst = '0' + bin(int(index))[2:].zfill(15)
        elif(instruction[1:] in RAMsymbols):
            index = RAMsymbols[instruction[1:]]
            ainst = '0' + bin(int(index))[2:].zfill(15)
        else:
            if(instruction[1:] in labels):
                index = labels[instruction[1:]]
                ainst = '0' + bin(int(index))[2:].zfill(15)
    else:
        ainst = '0' + bin(int(instruction[1:]))[2:].zfill(15)
    return ainst

#Converts a C instruction.
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
    return f'111{HandleCompInstruction(comp)}{mapVars.destMap[dest]}{mapVars.jumpMap[jump]}'

# Manages the six bit computation instruction
def HandleCompInstruction(instruction):
    comp = ""
    if(instruction in mapVars.compAzero.keys()):
        comp = '0' + mapVars.compAzero[instruction]
    elif(instruction in mapVars.compAone.keys()):
        comp = '1' + mapVars.compAone[instruction]
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

findLabels(instructions)
findRAMAddresses(instructions)
instructions = clearLabels(instructions)
parsedInstructions = Parser(instructions)

parsedInstructions = list(filter(None, parsedInstructions))
f.close()

#Writing to file.
with open(outfileName, 'w') as g:
    for line in parsedInstructions:
        g.write(f"{line}\n")
