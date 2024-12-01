# https://adventofcode.com/2023/day/20

from math import lcm

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

def find_sources(modules, name):
	return [source_name for source_name, module in modules.items() if name in module[2]]

def process_pulse(modules, pulses, i, records):
	while len(pulses) > 0:
		sender, pulse_destination, pulse_value = pulses.pop(0)
		if sender in records and pulse_value == True:
			records[sender].append(i)

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
			value = any([not value for value in module[1].values()])
			for destination in module[2]:
				pulses.append((pulse_destination, destination, value))

def solve(filename):
	modules = parse_input(filename)
	if DEBUG:
		for name, module in modules.items(): print(name, module)

	rx_sources = find_sources(modules, 'rx')
	if DEBUG: print('rx_sources', rx_sources)
	if len(rx_sources) != 1 or modules[rx_sources[0]][0] != '&':
		raise ValueError('Only one & source expected for rx')

	rx_source_sources = find_sources(modules, rx_sources[0])
	if DEBUG: print('rx_source_sources', rx_source_sources)
	if any([modules[name][0] != '&' for name in rx_source_sources]):
		raise ValueError('Only & sources expected for rx\'s source')

	records = dict([(name, []) for name in rx_source_sources])

	for i in range(1, 50_000):
		process_pulse(modules, [(None, 'broadcaster', False)], i, records)
	
	for name, record in records.items():
		print(name, record)
		for i, value in enumerate(record[1:]):
			if value - record[i] != record[0]:
				raise ValueError('Expected a constant interval for', name)

	button_presses = lcm(*[record[0] for record in records.values()])
	print(filename, 'button_presses to False -> rx', button_presses)

DEBUG = True
solve('20_input.txt')
