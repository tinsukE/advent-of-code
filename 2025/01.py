# https://adventofcode.com/2025/day/1

def parse_input(filename):
	file = open(filename, 'r')
	rotations = []
	for line in [line.strip() for line in file.readlines()]:
		a = line[0]
		b = line[1:]
		rotations.append([a, int(b)])
	return rotations

def solve_1(filename):
	rotations = parse_input(filename)

	dial = 50
	password = 0
	for rotation in rotations:
		if rotation[0] == 'L':
			dial -= rotation[1]
		else:
			dial += rotation[1]

		if (dial % 100) == 0:
			password += 1

	print("password", password)

def solve_2(filename):
	rotations = parse_input(filename)

	dial = 50
	password = 0
	for rotation in rotations:
		if rotation[0] == 'L':
			calcDial = (100 - dial) % 100
			calcDial += rotation[1]
			password += calcDial // 100

			dial -= rotation[1]
		else:
			dial += rotation[1]
			if dial > 99:
				password += dial // 100

		dial %= 100

	print("password", password)


solve_1('01_sample.txt') # 3
solve_1('01_input.txt') # 1018

solve_2('01_sample.txt') # 6
solve_2('01_input.txt') # 5815
