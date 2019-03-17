
from assembler_files.instructions import *
from vm_files.registers import *
from vm_files.stack import *
import sys

class opcode_builder:
	def __init__(self, opcode, label):
		self.label = label
		self.opcode = opcode
		self.function = []

	def write_register(self, machine, registers, args, context=None):
		write_value = context
		if(write_value == None):
			if(6 <= args[1]):
				write_value = machine.fetch()
			else:
				write_value = args[4]
		registers.get_register(args[1])(write_value)

	def argument_value(self, registers, machine, args):
		if(args[4] == 5):
			return registers.get_register(args[1], read=True)
		if(6 <= args[1] and args[3] == 9):
			return machine.fetch()
		else:
			return args[4]

	def jmp_check(self, machine, args):
		if(args[4] == 1):
			return 0
		else:
			return machine.fetch()

	def jmp(self):
		self.function.append(lambda machine, registers, args, context : self.jmp_check(machine, args))
		return self

	def args_value(self):
		self.function.append(lambda machine, registers, args, context :	self.argument_value(registers, machine, args))
		return self

	def save(self, register=None):
		if(register == None):
			self.function.append(lambda machine, registers, args, context : self.write_register(machine, registers, args, context))
		else:
			self.function.append(lambda machine, registers, args, context : registers.setPC(context))
		return self

	def XOR(self):
		self.function.append(lambda machine, registers, args, context : registers.get_register(args[2], read=True) ^ registers.get_register(args[3], read=True))
		return self

	def AND(self):
		self.function.append(lambda machine, registers, args, context : registers.get_register(args[2], read=True) & registers.get_register(args[3], read=True))
		return self

	def OR(self):
		self.function.append(lambda machine, registers, args, context : registers.get_register(args[2], read=True) | registers.get_register(args[3], read=True))
		return self

	def add(self):
		self.function.append(lambda machine, registers, args, context : registers.get_register(args[2], read=True) + registers.get_register(args[3], read=True))
		return self

	def sub(self):
		self.function.append(lambda machine, registers, args, context : registers.get_register(args[2], read=True) - registers.get_register(args[3], read=True))
		return self

	def cmp(self):
		self.function.append(lambda machine, registers, args, context : int(registers.get_register(args[2], read=True) == registers.get_register(args[3], read=True)))
		return self

	def push(self):
		self.function.append(lambda machine, registers, args, context : self.argument_value(registers, machine, args))
		self.function.append(lambda machine, registers, args, context : machine.stack.push(context))
		self.function.append(lambda machine, registers, args, context : registers.incrementSP())
		return self

	def pop(self):
		self.function.append(lambda machine, registers, args, context : machine.stack.pop())
		self.function.append(lambda machine, registers, args, context : registers.decrementSP())
		return self

	def jump_equal(self):
		self.function.append(lambda machine, registers, args, context : context if(registers.F == 1) else registers.PC)
		return self		

	def jump_not_equal(self):
		self.function.append(lambda machine, registers, args, context : context if(registers.F == 0) else registers.PC)		
		return self		


class opcodes:
	def __init__(self):
		self.opcodes = [None] * 0xF

	def register(self, opcode, label):
		self.opcodes[opcode] = opcode_builder(opcode, label)
		return self.opcodes[opcode]

	def build(self):
		self.register(instruction_id["lr"], "lr").args_value().save()
		self.register(instruction_id["xor"], "xor").XOR().save()
		self.register(instruction_id["and"], "and").AND().save()
		self.register(instruction_id["or"], "or").OR().save()
		self.register(instruction_id["cmp"], "cmp").cmp().save()		
		self.register(instruction_id["jmp"], "jmp").jmp().save("PC")
		
		self.register(instruction_id["je"], "je").jmp().jump_equal().save("PC")
		self.register(instruction_id["jne"], "jne").jmp().jump_not_equal().save("PC")


		self.register(instruction_id["add"], "add").add().save()
		self.register(instruction_id["sub"], "sub").sub().save()		
		self.register(instruction_id["push"], "push").push()
		self.register(instruction_id["pop"], "pop").pop().save()
		return self

	def decode_opcode(self, opcode):
		instruction_id = (opcode & 0xF000) >> 12
		byte_val = (opcode & 0xFF)	

		argument_1 = (opcode & 0xF00) >>  8
		argument_2 = (opcode & 0xF0) >>  4
		argument_3 = (opcode & 0xF)

		return (instruction_id, argument_1, argument_2, argument_3, byte_val)

	def execute(self, machine, opcode):
		opcode = self.decode_opcode(opcode)
		print("Opcode == {}".format(self.opcodes[opcode[0]].label))
		context = None
		for i in range(len(self.opcodes[opcode[0]].function)):
			opcode_id = opcode[0]						
			results = self.opcodes[opcode_id].function[i](machine, machine.registers, [opcode_id, opcode[1], opcode[2], opcode[3], opcode[4]], context)
			if not results == None:
				context = results

class machine:
	def __init__(self, file_instructions):
		self.registers = registers()
		self.stack = stack()
		self.opcode = opcodes().build()
		self.instructions = file_instructions
		self.running = True

	def fetch(self):
		next_instruction = self.instructions[self.registers.PC]
		if(self.registers.PC < len(self.instructions) - 1):
			self.registers.PC += 1
		else:
			self.running = False
		return next_instruction

	def check_state(self):
		if(self.registers.PC < len(self.instructions) - 1):
			self.running = True

	def execute(self):
		while self.running:
			current_opcode = self.fetch()
			self.opcode.execute(self, current_opcode)
			self.registers.print_values()
			self.stack.print_values()
			self.check_state()
			print("")
		print("Done")

def int_from_bytes(byte):
	return int.from_bytes(byte, 'big')

if __name__ == "__main__":
	if(len(sys.argv) == 2):
		encoding = open(sys.argv[1], "rb")

		file_parsed = []
		two_bytes = encoding.read(1) + encoding.read(1)
		instruction = int_from_bytes(two_bytes)
		while True:
			if not instruction:
				break
			file_parsed.append(instruction)
			two_bytes = encoding.read(1) + encoding.read(1)
			instruction = int_from_bytes(two_bytes)

		if((2 ** 16 - 1) < len(file_parsed)):
			raise Exception("File is too large")
		
		machine(file_parsed).execute()
	else:
		print("vm.py [file]")
