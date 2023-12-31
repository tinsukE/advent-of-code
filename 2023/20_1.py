# https://adventofcode.com/2023/day/20

def parse_input(filename):
	modules = {}

	file = open(filename, 'r')
	for line in file.readlines():
		name, destinations = line.strip().split(' -> ')
		kind = name[0]
		name = name if kind == 'b' else name[1:]

		state = None
		if kind == '%':
			state = False
		elif kind == '&':
			state = {}

		modules[name] = (kind, state, destinations.split(', '))

	for key, module in modules.items():
		for destination in module[2]:
			if destination in modules and modules[destination][0] == '&':
				modules[destination][1][key] = False

	return modules

def count_pulses(modules, pulses):
	sum_lows = 0
	sum_highs = 0

	while len(pulses) > 0:
		sender, pulse_destination, pulse_value = pulses.pop(0)
		# print(sender, '-', pulse_value, '->', pulse_destination)
		if pulse_value:
			sum_highs += 1
		else:
			sum_lows += 1

		module = modules.get(pulse_destination)
		if module == None:
			continue
		if module[0] == 'b':
			for destination in module[2]:
				pulses.append((pulse_destination, destination, pulse_value))
		elif module[0] == '%':
			if pulse_value == False:
				value = not module[1]
				modules[pulse_destination] = (module[0], value, module[2])
				for destination in module[2]:
					pulses.append((pulse_destination, destination, value))
		elif module[0] == '&':
			module[1][sender] = pulse_value
			# print(module)
			value = any([not value for value in module[1].values()])
			for destination in module[2]:
				pulses.append((pulse_destination, destination, value))

	return sum_lows, sum_highs

def solve_1(filename):
	modules = parse_input(filename)
	# print(modules)

	sum_lows = 0
	sum_highs = 0
	for _ in range(1000):
		lows, highs = count_pulses(modules, [(None, 'broadcaster', False)])
		sum_lows += lows
		sum_highs += highs
	print(filename, 'lows * highs =', sum_lows * sum_highs)

solve_1('20_sample1.txt')
solve_1('20_sample2.txt')
solve_1('20_input.txt')
