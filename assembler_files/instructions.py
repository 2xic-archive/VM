instruction_set = {
	"lr":["registers", "int"],
	"jmp":["label"],
	"push":[	
			["int", "registers"] 	
			],
	"pop":["registers"],
	"xor":["registers", "registers", "registers"],
	"cmp":["registers", "registers"],
	"jne":["label"],
	"add":["registers", "registers", "registers"],
	"sub":["registers", "registers", "registers"],
	"and":["registers", "registers", "registers"],
	"or":["registers", "registers", "registers"],
	"cmp":["registers", "registers"],
	"je":["label"],
	"jne":["label"]
}

instruction_id = {
	"cmp":0x0,
	"lr":0x1,
	"jmp":0x2,
	"push":0x3,
	"pop":0x4,
	"xor":0x5,
	"add":0x6,
	"sub":0x7,
	"and":0x8,
	"or":0x9,
	"je":0xa,
	"jne":0xb
}

registers_id = {
	"a":0,
	"b":1,
	"c":2,
	"d":3,
	"e":4,
	"f":5,

	"ab":6,
	"cd":7,
	"ef":8
}