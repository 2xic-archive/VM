
class stack_element:
	def __init__(self, data):
		self.data = data
		self.next = None
		self.position = 0

class stack:
	def __init__(self):
		self.top = None
 
	def push(self, data):		
		if self.top is None:
			self.top = stack_element(data)
		else:
			if(255 < self.top.position + 1):
				raise Exception("Stack overflow")
			next_element = stack_element(data)
			next_element.next = self.top
			next_element.position = self.top.position + 1
			self.top = next_element

	def pop(self):
		if self.top is None:
			raise Exception("Stack is empty")
		else:
			popped = self.top.data
			self.top = self.top.next
			return popped

	def print_values(self):
		position = self.top
		while position != None:
			print(position.data, end="->")
			position = position.next
		print("")