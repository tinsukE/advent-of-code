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
		gates.append([gate[0].split(' '), gate[1]])
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
	gates = list(gates)
	while len(gates):
		i = 0
		len_gates = len(gates)
		while i < len(gates):
			gate = gates[i]
			a = values.get(gate[0][0], None)
			b = values.get(gate[0][2], None)
			if a is not None and b is not None:
				values[gate[1]] = calculate_gate(gate[0][1], a, b)
				del gates[i]
				continue
			i += 1
		if len_gates == len(gates):
			break
	return values

def gates_value(values, char):
	z_wires = [wire for wire in values.keys() if wire[0] == char]
	z_wires.sort(reverse=True)

	number_bin = ['1' if values[z_wire] else '0' for z_wire in z_wires]
	return int(''.join(number_bin), 2)

def solve(filename):
	initials, gates = parse_input(filename)

	values = solve_gates(initials, gates)
	number = gates_value(values, 'z')
	print('number', number)

def print_addition(values, gates):
	x = gates_value(values, 'x')
	y = gates_value(values, 'y')
	z = gates_value(values, 'z')
	print(f'\n    x:  {x:045b}')
	print(f'    y:  {y:045b}')
	print(f'out_z: {z:046b}')
	print(f'exp_Z: {x + y:046b}')

	if z == x + y:
		print('🎄 the gates are correct!')
		return

	out_z_bin = f'0b{z:046b}'
	exp_z_bin = f'0b{x + y:046b}'
	for i in range(len(out_z_bin)):
		if out_z_bin[-i - 1] != exp_z_bin[-i - 1]:
			print('first different bit at:', i)
			return

def swap_wires(gates, a, b):
	gate_a = next(gate for gate in gates if gate[1] == a)
	gate_b = next(gate for gate in gates if gate[1] == b)
	print('swap wires for gates:', gate_a, 'and', gate_b)
	gate_a[1] = b
	gate_b[1] = a
	return set([a, b])

def solve_2(filename):
	# Any bit is determine by this form:
	# z02 = (y02 XOR x02) XOR ((x01 AND y01) OR (ktt AND rvb))
	# Where ktt and rvb are values used in the previous bit (less -> most significant)
	# This allows us to inspect the sample addition (less -> most),
	# find which bit is incorrect and manually determine which ports to swap.
	# Rinse and repeat until the gates are fixed

	initials, gates = parse_input(filename)
	swapped_wires = set()

	values = solve_gates(initials, gates)
	print_addition(values, gates)

	swapped_wires |= swap_wires(gates, 'z12', 'djg')

	values = solve_gates(initials, gates)
	print_addition(values, gates)

	swapped_wires |= swap_wires(gates, 'z19', 'sbg')

	values = solve_gates(initials, gates)
	print_addition(values, gates)

	# 24
	swapped_wires |= swap_wires(gates, 'mcq', 'hjm')

	values = solve_gates(initials, gates)
	print_addition(values, gates)

	swapped_wires |= swap_wires(gates, 'z37', 'dsd')

	values = solve_gates(initials, gates)
	print_addition(values, gates)

	print('\nswapped_wires', ','.join(sorted(list(swapped_wires))))

solve('24_sample.txt') # 4
solve('24_sample2.txt') # 2024
solve('24_input.txt') # 64755511006320

solve_2('24_input.txt')
