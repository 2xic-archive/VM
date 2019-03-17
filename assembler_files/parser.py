from .instructions import *

class lexer:
	def __init__(self, input_string):
		self.max_position = len(input_string)
		self.position = 0

		self.input_string = input_string
		self.current_char = self.input_string[self.position]
		self.current_line = 1

	def next(self):
		self.position += 1
		if(self.position >= self.max_position):
			self.current_char = None
		else:
			self.current_char = self.input_string[self.position]
		return self.current_char

	def peek(self):
		if(self.max_position <= self.position + 1):
			return None
		return self.input_string[self.position + 1]

class Token:
	def __init__(self, token_type, value, opcode_label=None):
		self.type = token_type
		self.value = value
		self.opcode_label = opcode_label

class node:
	def __init__(self, token):
		self.token = token
		self.right = None
		self.left = None

class AST:
	def __init__(self, string):
		self.lexer = lexer(string)

	def skip_space(self):
		while self.lexer.current_char == '\t' or self.lexer.current_char == ' ' or self.lexer.current_char == '\n':
			if(self.lexer.current_char == '\n'):
				self.lexer.current_line += 1
			self.lexer.next()

	def skip_one_line(self):
		while self.lexer.current_char != '\n':
			self.lexer.next()
		self.lexer.current_line += 1

	def get_text(self):
		text = ""
		while self.lexer.current_char != None and self.lexer.current_char.isalpha():
			text += self.lexer.current_char
			self.lexer.next()
		return text

	def get_hex(self):
		hexvalue = ""
		while self.lexer.current_char != None and (self.lexer.current_char.isalpha() or self.lexer.current_char.isdigit()):
			hexvalue += self.lexer.current_char
			self.lexer.next()
		return int(hexvalue, 16)

	def get_digit(self):
		digit = ""
		while self.lexer.current_char != None and self.lexer.current_char.isdigit():
			digit += self.lexer.current_char
			self.lexer.next()
		return int(digit)

	def get_next_token(self):
		self.skip_space()		
		if(self.lexer.current_char == None):
			return None

		if(self.lexer.current_char.isalpha()):
			data = self.get_text()
			if data in instruction_set.keys():
				return Token("instruction", instruction_id[data]  , data)
			elif data in registers_id.keys():
				return Token("registers", registers_id[data], data)
			return Token("label", data)
		elif(self.lexer.current_char.isdigit() and self.lexer.peek() == "x"):
			return Token("int", self.get_hex())
		elif(self.lexer.current_char.isdigit()):
			return Token("int", self.get_digit())
		elif(self.lexer.current_char == ","):
			self.lexer.next()
			return Token("comma", ",")
		elif(self.lexer.current_char == ":"):
			data = self.lexer.current_char
			self.lexer.next()
			return Token(data, ":")
		elif(self.lexer.current_char == "/"):
			self.lexer.next()
			if(self.lexer.current_char == "/"):
				self.skip_one_line()
				self.lexer.next()
				return self.get_next_token()
			else:
				raise Exception("fake comment")
		else:
			raise Exception("don't understand input")
		
	def expected_next(self, expected_token_type):
		next_token = self.get_next_token()
		if(next_token == None):
			return None
		if(next_token.type in expected_token_type):
			return next_token
		else:
			raise Exception("Line : {}, expected {}, but got {}".format(self.lexer.current_line, expected_token_type, next_token.type))

	def check_syntax(self, next_token_type, expected_token_type, last_token_type):
		if(next_token_type == None):
			raise Exception("Line : {}, expected {} after {}".format(self.lexer.current_line, expected_token_type, last_token_type))

	def parse_tokens(self):
		self.skip_space()

		token = self.get_next_token()

		if(token == None):
			return None
		elif(token.type == "instruction"):			
			head = node(token)
			leaf = head

			last_token_type = token.type
			for index in range(len(instruction_set[token.opcode_label])):
				next_token_type = instruction_set[token.opcode_label][index]
				next_token = self.expected_next(next_token_type)

				self.check_syntax(next_token, instruction_set[token.opcode_label][index], last_token_type)

				leaf.right = node(next_token)
				leaf = leaf.right
				last_token_type = next_token.type

				if not (len(instruction_set[token.opcode_label]) - 1) == index:
					self.check_syntax(self.expected_next("comma"), "comma", last_token_type)
					last_token_type = "comma"

			return head

		elif(token.type == "label"):
			head = node(token)	
			self.check_syntax(self.expected_next(":"), ":", "label")
			return head

	def parse(self):
		head = self.parse_tokens()
		leaf = head
		while True:
			next_leaf = self.parse_tokens()
			if(next_leaf == None):
				break
			leaf.left = next_leaf
			leaf = leaf.left			
		return head



