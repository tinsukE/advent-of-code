# https://adventofcode.com/2024/day/17

from dataclasses import dataclass, field

@dataclass
class Computer:
	a: int
	b: int
	c: int
	program: tuple
	pointer: int = field(default=0)

	def reset(self, a = None, b = None, c = None):
		self.pointer = 0
		self.a = a if a is not None else 0
		self.b = b if b is not None else 0
		self.c = c if c is not None else 0

	def combo(self, operand) -> int:
		if operand >= 0 and operand <= 3:
			return operand
		elif operand == 4:
			return self.a
		elif operand == 5:
			return self.b
		elif operand == 6:
			return self.c
		else:
			raise ValueError('Unexpected operand', operand)

	def compute(self) -> int:
		while self.pointer < len(self.program) - 1:
			instruction = self.program[self.pointer]
			operand = self.program[self.pointer + 1]

			if instruction == 0:
				self.a = int(self.a / (2 ** self.combo(operand)))
			elif instruction == 1:
				self.b = self.b ^ operand
			elif instruction == 2:
				self.b = self.combo(operand) % 8
			elif instruction == 3:
				if self.a != 0:
					self.pointer = operand
					continue
			elif instruction == 4:
				self.b = self.b ^ self.c
			elif instruction == 5:
				self.pointer += 2
				return self.combo(operand) % 8
			elif instruction == 6:
				self.b = int(self.a / (2 ** self.combo(operand)))
			elif instruction == 7:
				self.c = int(self.a / (2 ** self.combo(operand)))
			self.pointer += 2
		return None

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()

	registers = [int(line.split(': ')[1]) for line in lines[0:3]]
	program = [int(number) for number in lines[4].split(': ')[1].split(',')]
	
	return Computer(registers[0], registers[1], registers[2], program)

def solve(filename):
	computer = parse_input(filename)

	outputs = []
	while True:
		output = computer.compute()
		if output is None:
			break
		outputs.append(output)
	print('output', ','.join([str(output) for output in outputs]))

def solve_2(filename):
	computer = parse_input(filename)
	# print(" " * 18, computer.program)

	i = len(computer.program) - 1
	a = 0
	while i >= 0:
		computer.reset(a = a)
		outputs = []
		while True:
			output = computer.compute()
			if output is None:
				break
			outputs.append(output)
		if len(outputs) == len(computer.program):
			i = len(computer.program) - 1
			while i >= 0 and outputs[i] == computer.program[i]:
				# print(f'{a:015d}', f'{i:02d}', outputs)
				i -= 1
		a += int(8 ** i)

	# print(' ' * 18, computer.program)
	print('a', a)

solve('17_sample.txt') # 4,6,3,5,6,3,5,2,1,0
solve('17_input.txt') # 7,3,5,7,5,7,4,3,0

solve_2('17_sample2.txt') # 117440
solve_2('17_input.txt') # 105734774294938
