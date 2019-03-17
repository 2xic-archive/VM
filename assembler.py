from assembler_files.parser import *
import sys

def write_n_bits(output, values, current_bit_index, bits_length):
	values_list = []
	bits_length_list = []
	if(type(values) == int and type(bits_length) == int):
		values_list.append(values)
		bits_length_list.append(bits_length)
	elif(type(values) == list and type(bits_length) == list):
		values_list = values
		bits_length_list = bits_length
	else:
		raise Exception("Be consistent with arguments")

	assert (len(values_list) == len(bits_length_list))

	for index in range(len(values_list)):
		current_input = values_list[index]
		for i in range(bits_length_list[index], -1, -1):
			shift = current_input >> i
			if(shift & 1):
				output |= 1 << current_bit_index
			else:
				output |= 0 << current_bit_index
			current_bit_index -= 1
	
	if not current_bit_index == -1:
		raise Exception("Need to fill buffer")
	
	return output

def get_labels(parse_tree):
	labels = {

	}	
	tree_node = parse_tree
	byte_number = 0
	while True:
		if(tree_node.left != None):
			if(tree_node.token.type == "label"):
				labels[tree_node.token.value] = byte_number
			elif(tree_node.token.opcode_label in ["lr", "push"]):
				if(tree_node.right.token.type == "registers" or tree_node.right.token.value <= 255 ):
					byte_number += 1
				else:
					byte_number += 2
			elif(tree_node.token.opcode_label == "jmp" or tree_node.token.opcode_label == "jne" or tree_node.token.opcode_label == "je"):
				if(tree_node.right.token.value in labels.keys() and labels[tree_node.right.token.value] == 0):
					byte_number += 1
				else:
					byte_number += 2
			else:
				byte_number += 1
			tree_node = tree_node.left
		else:
			break
	return labels

def write_file(parse_tree, labels, outputfile):
	tree_node = parse_tree

	while tree_node != None:
		if(tree_node.token.type == "label"):
			tree_node = tree_node.left
			continue
		args_leaf = tree_node.right
		if(tree_node.token.opcode_label == "lr"):
			if(args_leaf.token.value >= 6):
				if (255 < args_leaf.right.token.value < (2 ** 16 - 1)):
					instruction = write_n_bits(0, [int(tree_node.token.value), int(args_leaf.token.value), 9], 15, [3, 3, 7])
					outputfile.write(instruction.to_bytes(2, byteorder='big'))

					instruction = write_n_bits(0, [int(args_leaf.right.token.value)], 15, [15])
					outputfile.write(instruction.to_bytes(2, byteorder='big'))
				elif(0 <= args_leaf.right.token.value <= 255):
					instruction = write_n_bits(0, [int(tree_node.token.value), int(args_leaf.token.value), int(args_leaf.right.token.value)], 15, [3, 3, 7])
					outputfile.write(instruction.to_bytes(2, byteorder='big'))
				else:
					raise Exception("to big number")			
			else:
				if not (args_leaf.right.token.value <= 255):
					raise Exception("maximum is 8 bits for 8 bit registers ")
				instruction = write_n_bits(0, [int(tree_node.token.value), int(args_leaf.token.value), int(args_leaf.right.token.value)], 15, [3, 3, 7])
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
			
		elif(tree_node.token.opcode_label == "push"):
			if(args_leaf.token.type == "registers"):
				instruction = write_n_bits(0, [int(tree_node.token.value), int(args_leaf.token.value), 5], 15,  [3, 3, 7])			
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
			else:
				if(args_leaf.token.value <= 255):
					instruction = write_n_bits(0, [int(tree_node.token.value), 0, int(args_leaf.token.value) ], 15,  [3, 3, 7])			
					outputfile.write(instruction.to_bytes(2, byteorder='big'))
				elif(args_leaf.token.value <= (2**16-1)):
					instruction = write_n_bits(0, [int(tree_node.token.value),  int(args_leaf.token.value), 9 ], 15,  [3, 3, 7])			
					outputfile.write(instruction.to_bytes(2, byteorder='big'))

					instruction = write_n_bits(0, int(args_leaf.token.value), 15,  15)					
					outputfile.write(instruction.to_bytes(2, byteorder='big'))
				else:
					raise Exception("illegal !")

		elif(tree_node.token.opcode_label == "pop"):
			instruction = write_n_bits(0, [int(tree_node.token.value), int(args_leaf.token.value), 0 ], 15,  [3, 3, 7])
			outputfile.write(instruction.to_bytes(2, byteorder='big'))
		elif(tree_node.token.opcode_label == "jmp"):
			if(int(labels[tree_node.right.token.value]) == 0):
				instruction = write_n_bits(0, [int(tree_node.token.value), 0, 1], 15,  [3, 3, 7])			
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
			else:			
				instruction = write_n_bits(0, [int(tree_node.token.value), 0, 0], 15,  [3, 3, 7])			
				outputfile.write(instruction.to_bytes(2, byteorder='big'))

				instruction = write_n_bits(0, int(labels[tree_node.right.token.value]), 15,  15)			
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
		elif(tree_node.token.opcode_label in ["xor", "add", "sub", "and", "or"]):
			values = [int(tree_node.token.value)]
			while args_leaf != None:
				values.append(int(args_leaf.token.value))
				args_leaf = args_leaf.right
			instruction = write_n_bits(0, values, 15,  [3, 3, 3, 3])
			outputfile.write(instruction.to_bytes(2, byteorder='big'))
		elif(tree_node.token.opcode_label == "cmp"):
			instruction = write_n_bits(0, [int(tree_node.token.value), int(registers_id["f"]), int(args_leaf.token.value), int(args_leaf.right.token.value)], 15,  [3, 3, 3, 3])
			outputfile.write(instruction.to_bytes(2, byteorder='big'))
		elif(tree_node.token.opcode_label == "je" or tree_node.token.opcode_label == "jne"):
			if(int(labels[tree_node.right.token.value]) == 0):
				instruction = write_n_bits(0, [int(tree_node.token.value), 2, 1], 15,  [3, 3, 7])
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
			else:
				instruction = write_n_bits(0, [int(tree_node.token.value), 2, 0], 15,  [3, 3, 7])
				outputfile.write(instruction.to_bytes(2, byteorder='big'))

				instruction = write_n_bits(0, int(labels[tree_node.right.token.value]), 15,  15)
				outputfile.write(instruction.to_bytes(2, byteorder='big'))
		else:
			raise Exception("Code in the fucntion")

		tree_node = tree_node.left
	outputfile.close()

if __name__ == "__main__":
	if(len(sys.argv) == 3):
		in_file = open(sys.argv[1], "r").read()
		out_file = open(sys.argv[2], "wb")
		
		if(len(in_file) == 0):
			raise Exception("No content in file")

		parse_tree = AST(in_file).parse()
		labels = get_labels(parse_tree)

		write_file(parse_tree, labels, out_file)
		print("Success")
	else:
		print("assembler.py	[in file]	[out file]")


