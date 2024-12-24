# https://adventofcode.com/2024/day/24

def parse_input(filename):
	file = open(filename, 'r')

	initials = {}
	line = file.readline().strip()
	while len(line):
		value = line.split(': ')
		initials[value[0]] = value[1] == '1'
		line = file.readline().strip()

	gates = []
	line = file.readline().strip()
	while len(line):
		gate = line.split(' -> ')
		gates.append((gate[0].split(' '), gate[1]))
		line = file.readline().strip()

	return (initials, gates)

def calculate_gate(op, a, b):
	if op == 'AND':
		return a and b
	if op == 'OR':
		return a or b
	if op == 'XOR':
		return a ^ b
	raise ValueError("Unsupported operation", op)

def solve_gates(initials, gates):
	values = dict(initials)
	while len(gates):
		i = 0
		while i < len(gates):
			gate = gates[i]
			a = values.get(gate[0][0], None)
			b = values.get(gate[0][2], None)
			if a is not None and b is not None:
				values[gate[1]] = calculate_gate(gate[0][1], a, b)
				del gates[i]
				continue
			i += 1
	return values

def gates_output(values):
	z_wires = [wire for wire in values.keys() if wire[0] == 'z']
	z_wires.sort(reverse=True)

	number_bin = ['1' if values[z_wire] else '0' for z_wire in z_wires]
	return int(''.join(number_bin), 2)

def solve(filename):
	initials, gates = parse_input(filename)

	values = solve_gates(initials, gates)
	number = gates_output(values)
	print('number', number)

# def solve_2(filename, swaps):
# 	initials, gates = parse_input(filename)

# 	bits = sum(1 for line in initials.keys() if line[0] == 'x')
# 	print('bits', bits, 1 << bits)


solve('24_sample.txt') # 4
solve('24_sample2.txt') # 2024
solve('24_input.txt') # 64755511006320

# solve_2('24_sample3.txt', 2)
# solve_2('24_input.txt', 4)
