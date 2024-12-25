# https://adventofcode.com/2024/day/25

def parse_item(lines):
	depths = []
	for depth in range(len(lines[0])):
		for i in range(len(lines)):
			if lines[i][depth] != '#':
				depths.append(i)
				break
	return depths


def parse_input(filename):
	file = open(filename, 'r')
	locks = []
	keys = []
	length = None

	line = file.readline().strip()
	while line:
		lines = [line]
		line = file.readline().strip()
		while line:
			if len(line) > 0:
				lines.append(line)
			else:
				break
			line = file.readline().strip()

		if lines[0][0] == '#':
			locks.append(parse_item(lines[1:]))
		elif lines[0][0] == '.':
			keys.append(parse_item(lines[-2::-1]))
		if length is None:
			length = len(lines) - 2
		line = file.readline().strip()

	return length, locks, keys

def solve(filename):
	length, locks, keys = parse_input(filename)
	# print('length', length)
	# print('locks', locks)
	# print('keys', keys)

	fits = 0
	for lock in locks:
		for key in keys:
			if all([lock[d] + key[d] <= length for d in range(len(lock))]):
				fits += 1
	print('fits', fits)

solve('25_sample.txt') # 3
solve('25_input.txt') # 3508