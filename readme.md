# VM
Includes code for an assembler for a assembly like language and a VM to run the binary produced by the assembler.

## Registers
**A**, **B**, **C**, **D**, **E** and **F** are all 8 bit registers. However by design the VM has support for grouped registers that is **AB**, **CD** and **EF** to form 16 bit registers. The **PC** is a 16 bit register as well. **F** is a special register, it used a flag register for **cmp**. 

##  Instruction encoding
Instructions are encoded as 2 bytes. Mainly like the way described in the table below. 

| 4 bit      		 	| 4 bit           		| 4 bit  				| 4 bit  |
| ------------- 		|:-------------:		| :-----:				| :----------:| 
| **instruction id**     | register or integer	| register 	or integer	| register	or integer

Obviously if the instruction doesn't require 3 arguments the last bits will be zero. Some instructions are special like the **jmp**, it requires that another 16 bit is fetched (if the jump location isn’t at PC=0). Meaning that the VM first will read the instruction

| 4 bit       		| 4 bit           	| 4 bit  	| 4 bit  		|
| ------------- 	|:-------------:	| :-------:	| :----------:	| 
| **jmp**      		| 0					| 0 		| 0	  			|

then it will fetch the next instruction with the location.

| 16 bit  					|
| ---------------- 			| 
| **jmp location**      	|

**push** works the same way if the value pushed onto the stack is greater than 8 bits. 

## Instruction set
| Instruction       | Argument 1           	| Argument 2  	| Argument 3  |	Action  						| Notes  		|
| ------------- 	|:-------------:		| :-----:		| :----------:| :--------------------:			| :----------:	|
| **lr**      		| register				| integer 		| *None*	  | Loads registers with value 		| *None* 		|
| **push**      	| register	or	integer	| *None* 		| *None*	  | Push value onto the stack 		| *None* 		|
| **pop**      		| register				| *None* 		| *None*	  | Pop value off the stack and into a register		| Can only pop 16 bit values to a 16 bit registers.  		|
| **add**      		| register				| register 		| register	  | Addition 	| *None* 		|
| **sub**      		| register				| register 		| register	  | Subtraction 	| *None* 		|
| **and**      		| register				| register 		| register	  | Bitwise and 	| *None* 		|
| **or**      		| register				| register 		| register	  | Bitwise or 	| *None* 		|
| **xor**      		| register				| register 		| register	  | Bitwise xor 	| *None* 		|
| **cmp**      		| register				| register 		| *None*	  | Compare value of to registers 	| Results is saved to the F register.  		|
| **jne**      		| label				| *None* 		| *None*	  | Jump to a declared label if the comparison was not equal 	| Depends on value of the F register. Run cmp first.  		|
| **je**      		| label				| *None* 		| *None*	  | Jump to a declared label if the comparison was equal 	| Depends on value of the F register. Run cmp first.  		|
| **jmp**      		| label				| *None* 		| *None*	  | Jump to a declared label 	| *None*  		|

## Example code
Example code using a variety of the instruction set for the purpose of demonstration the VM in action. 
```
lr a, 10
lr c, 20
jmp middle

start:
	add a, b, b
	cmp a, c
	jne start
	je end

middle:
	lr b, 10
	cmp a, b
	je start

end:
	push c
	push ab
	push 255
	push 0xffff
	pop ef
```
