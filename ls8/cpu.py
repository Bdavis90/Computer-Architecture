"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0b00000000

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value
        
    def load(self):
        """Load a program into memory."""


        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        
        with open(sys.argv[1]) as f:
            for line in f:
                new_line = line.split('#')[0].strip()
                if new_line == '':
                    continue
                else:
                    bn = int(new_line, 2)
                    self.ram[address] = bn
                    address += 1

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.register[operand_a] *= self.register[operand_b]
                self.pc += 3
            elif IR == PUSH:
                self.register[SP] -= 1
                self.ram_write(self.register[SP], self.register[operand_a])
                self.pc += 2
            elif IR == POP:
                stack_value = self.ram_read(self.register[SP])
                self.register[operand_a] = stack_value
                self.register[SP] += 1
                self.pc += 2
            elif IR == CALL:
                return_address = self.pc + 2
                self.register[SP] -= 1
                self.ram[self.register[SP]] = return_address
                reg_num = self.ram[self.pc + 1]
                dest_addr = self.ram[reg_num]
                self.pc = dest_addr
            elif IR == RET:
                return_address = self.ram[self.register[SP]]
                self.register[SP] += 1
                self.pc = return_address
            elif IR == CMP:
                if self.register[operand_a] == self.register[operand_b]:
                    self.fl = 0b00000001
                if self.register[operand_a] > self.register[operand_b]:
                    self.fl = 0b00000010
                if self.register[operand_a] < self.register[operand_b]:
                    self.fl = 0b00000100
                self.pc += 3
            elif IR == JMP:
                self.pc = self.register[operand_a]
            elif IR == JEQ:
                address = self.register[operand_a]
                if self.fl == 1:
                    self.pc = address
                else:
                    self.pc += 2
            elif IR == JNE:
                address = self.register[operand_a]
                if self.fl == 0:
                    self.pc = address
                else:
                    self.pc += 2
            elif IR == HLT:
                running = False
            
