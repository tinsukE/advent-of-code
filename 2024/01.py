# https://adventofcode.com/2024/day/1

def parse_input(filename):
	file = open(filename, 'r')
	list_a = []
	list_b = []
	for line in [line.strip() for line in file.readlines()]:
		a, b = line.split('   ')
		list_a.append(int(a))
		list_b.append(int(b))
	return list_a, list_b

def solve_1(filename):
	list_a, list_b = parse_input(filename)
	list_a.sort()
	list_b.sort()

	diff = 0
	for (a, b) in zip(list_a, list_b):
		diff += abs(a - b)

	print("diff", diff)

def solve_2(filename):
	list_a, list_b = parse_input(filename)
	list_a.sort()
	list_b.sort()

	map_b = {}
	for b in list_b:
		map_b[b] = map_b.get(b, 0) + 1

	similarity = 0
	for a in list_a:
		similarity += a * map_b.get(a, 0)

	# print("map_b", map_b)
	print("similarity", similarity)

solve_1('01_sample.txt') # 11
solve_1('01_input.txt') # 1873376

solve_2('01_sample.txt') # 31
solve_2('01_input.txt') # 18997088
