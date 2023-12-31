# https://adventofcode.com/2023/day/20

from time import time

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

def process_pulse(modules, pulses):
	while len(pulses) > 0:
		sender, pulse_destination, pulse_value = pulses.pop(0)
		# print(sender, '-', pulse_value, '->', pulse_destination)

		if pulse_destination == 'rx' and not pulse_value:
			return True

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

	return False

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def solve(filename):
	modules = parse_input(filename)
	# print(modules)

	start = time()
	current_report_start = start

	button_presses = 0
	while True:
		button_presses += 1
		if process_pulse(modules, [(None, 'broadcaster', False)]):
			break

		current_time = time()
		if current_time - current_report_start > 5:
			current_report_start = current_time
			speed = button_presses / (current_time - start)
			print('button_presses', human_format(button_presses), '@', human_format(speed), '/s')
	print(filename, 'button_presses', button_presses)

solve('20_input.txt')
