
class registers:
	def __init__(self):
		self.A = 0
		self.B = 0
		self.C = 0
		self.D = 0
		self.E = 0
		self.F = 0
		self.PC = 0
		self.SP = 0

	def print_values(self):
		print("AB={}	CD={}	EF={}	PC={}	SP={}".format(self.getAB(), self.getCD(), self.getEF(), self.PC, self.SP))
		print("A={}	B={}	C={}	D={}	E={}	F={}".format(self.getA(),self.getB(), self.getC(),self.getD(), self.getE(),self.getF()))

	def setA(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register A")
		self.A = value

	def setB(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register B")
		self.B = value
	
	def setC(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register C")
		self.C = value
	
	def setD(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register D")
		self.D = value
	
	def setE(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register E")
		self.E = value

	def setF(self, value):
		if not ((0 <= value <= 0xff)):
			raise Exception("Bad byte in register F")
		self.F = value
	
	def setAB(self, value):
		if not (0 <= value <= 0xffff):
			raise Exception("Bad word to register AB")
		self.A = value >> 8
		self.B = value & 0xff
		
	def setCD(self, value):
		if not (0 <= value <= 0xffff):
			raise Exception("Bad word to register CD")
		self.C = value >> 8
		self.D = value & 0xff

	def setEF(self, value):
		if not (0 <= value <= 0xffff):
			raise Exception("Bad word to register EF")
		self.E = value >> 8
		self.F = value & 0xff

	def getA(self):
		return self.A

	def getB(self):
		return self.B
	
	def getC(self):
		return self.C
	
	def getD(self):
		return self.D
	
	def getE(self):
		return self.E

	def getF(self):
		return self.F
	
	def getAB(self):
		return self.getA() << 8 | self.getB()
		
	def getCD(self):
		return self.getC() << 8 | self.getD()

	def getEF(self):
		return self.getE() << 8 | self.getF()

	def incrementSP(self):
		self.SP += 1

	def decrementSP(self):
		self.SP -= 1

	def setPC(self, value):
		if(0 <= value):	
			self.PC = value
			
	def get_register(self, register_id, read=False):
		if(register_id == 0 and not read):
			return self.setA
		elif(register_id == 1 and not read):
			return self.setB
		elif(register_id == 2 and not read):
			return self.setC
		elif(register_id == 3 and not read):
			return self.setD
		elif(register_id == 4 and not read):
			return self.setE
		elif(register_id == 5 and not read):
			return self.setF
		elif(register_id == 6 and not read):
			return self.setAB
		elif(register_id == 7 and not read):
			return self.setCD
		elif(register_id == 8 and not read):
			return self.setEF
		elif(register_id == 0 and read):
			return self.getA()
		elif(register_id == 1 and read):
			return self.getB()
		elif(register_id == 2 and read):
			return self.getC()
		elif(register_id == 3 and read):
			return self.getD()
		elif(register_id == 4 and read):
			return self.getE()
		elif(register_id == 5 and read):
			return self.getF()
		elif(register_id == 6 and read):
			return self.getAB()
		elif(register_id == 7 and read):
			return self.getCD()
		elif(register_id == 8 and read):
			return self.getEF()
		else:
			raise Exception("Bug in get_register")
