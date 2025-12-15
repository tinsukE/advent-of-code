# https://adventofcode.com/2025/day/10

from scipy.optimize import linprog

def parse_buttons(buttons_str):
	button_groups = [button for button in buttons_str.strip().split(' ')]
	buttons = []
	for button_group in button_groups:
		buttons.append(set([int(button) for button in button_group[1:-1].split(',')]))
	return buttons

def parse_input(filename):
	file = open(filename, 'r')
	machines = []
	for line in [line.strip() for line in file.readlines()]:
		(lights, rest) = line.split(']')
		(buttons, joltages) = rest.split('{')
		lights = lights[1:]
		buttons = parse_buttons(buttons)
		joltages = tuple([int(joltage) for joltage in joltages[0:-1].split(',')])
		machines.append((lights, buttons, joltages))
	return machines

def press_button(state, button):
	new_state = []
	for i, light in enumerate(state):
		if i in button:
			new_state.append('.' if light == '#' else '#')
		else:
			new_state.append(light)
	return ''.join(new_state)

def solve_1(filename):
	machines = parse_input(filename)

	sum_presses = 0
	for (lights, buttons, _) in machines:
		initial_state = '.' * len(lights)
		all_states = set(initial_state)
		states = [(initial_state, 0)]

		min_presses = -1
		while len(states) > 0 and min_presses < 0:
			(state, presses) = states.pop(0)
			for button in buttons:
				new_state = press_button(state, button)
				if new_state == lights:
					min_presses = presses + 1
					break
				if new_state not in all_states:
					all_states.add(new_state)
					states.append((new_state, presses + 1))

		sum_presses += min_presses

	print('sum_presses', sum_presses)

def press_button_joltage(state, button):
	return tuple([number + 1 if i in button else number for i, number in enumerate(state)])

def distance_to(joltages, state):
	return sum([joltages[i] - state[i] for i in range(len(joltages))])

def solve_2(filename):
	machines = parse_input(filename)

	sum_presses = 0
	for (_, buttons, joltages) in machines:
		# naive
		# initial_state = (0,) * len(joltages)
		# all_states = set(initial_state)
		# states = [(initial_state, 0)]
		# min_presses = -1
		# while len(states) > 0 and min_presses < 0:
		# 	(state, presses) = states.pop(0)
		# 	for button in buttons:
		# 		new_state = press_button_joltage(state, button)
		# 		if new_state == joltages:
		# 			min_presses = presses + 1
		# 			break
		# 		if any([number > joltages[i] for i, number in enumerate(new_state)]):
		# 			break
		# 		if new_state not in all_states:
		# 			all_states.add(new_state)
		# 			states.append((new_state, presses + 1))
		# sum_presses += min_presses

		c = (1,) * len(buttons)
		A = []
		b = joltages

		for i, joltage in enumerate(joltages):
			row = []
			for button in buttons:
				row.append(1 if i in button else 0)
			A.append(row)

		# print('c', c)
		# print('A', A)
		# print('b', b)

		res = linprog(c, A_eq=A, b_eq=b, integrality=3)

		print('x', res.x)

		sum_presses += round(sum(res.x))

	print('sum_presses', sum_presses)

solve_1('10_sample.txt') # 7
solve_1('10_input.txt') # 441

solve_2('10_sample.txt') # 33
solve_2('10_input.txt') # ?
