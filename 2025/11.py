# https://adventofcode.com/2025/day/11

from functools import cache

def parse_input(filename):
	file = open(filename, 'r')
	devices = {}
	for line in [line.strip() for line in file.readlines()]:
		(device, outputs) = line.split(': ')
		devices[device] = tuple(outputs.split(' '))
	return devices

def paths_to_out(devices, device):
	sum_paths = 0
	for output in devices[device]:
		if output == 'out':
			sum_paths += 1
		else:
			sum_paths += paths_to_out(devices, output)
	return sum_paths

@cache
def paths_to_out_dac_fft(devices, device, visited_dac = False, visited_fft = False):
	if not visited_dac and device == 'dac':
		visited_dac = True
	if not visited_fft and device == 'fft':
		visited_fft = True

	sum_paths = 0
	for output in devices[device]:
		if output == 'out':
			sum_paths += 1 if visited_dac and visited_fft else 0
		else:
			sum_paths += paths_to_out_dac_fft(devices, output, visited_dac, visited_fft)
	return sum_paths

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))

def solve_1(filename):
	devices = parse_input(filename)

	sum_paths = paths_to_out(devices, 'you')
	print('sum_paths', sum_paths)

def solve_2(filename):
	devices = hashabledict(parse_input(filename))

	sum_paths = paths_to_out_dac_fft(devices, 'svr')
	print('sum_paths', sum_paths)

solve_1('11_sample.txt') # 5
solve_1('11_input.txt') # 590

solve_2('11_sample_2.txt') # 2
solve_2('11_input.txt') # ?
