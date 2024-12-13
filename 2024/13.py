# https://adventofcode.com/2024/day/13

import numpy

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	machines = []
	i = 0
	while i < len(lines):
		a = lines[i]
		b = lines[i + 1]
		prize = lines[i + 2]
		i += 4

		a = [int(number.strip().split('+')[1]) for number in a.split(',')]
		b = [int(number.strip().split('+')[1]) for number in b.split(',')]
		prize = [int(number.strip().split('=')[1]) for number in prize.split(',')]

		machines.append([a, b, prize])

	return machines

def solve(filename, offset = 0):
	machines = parse_input(filename)

	sum_cost = 0
	for m in machines:
		# https://www.statology.org/solve-system-of-equations-in-python/
		a = numpy.array([[m[0][0], m[1][0]], [m[0][1], m[1][1]]])
		b = numpy.array([m[2][0] + offset, m[2][1] + offset])
		result = numpy.linalg.solve(a, b)
		if all([x > 0 and abs(x - round(x)) < 0.001 for x in result]):
			sum_cost += round(result[0]) * 3 + round(result[1])

	print('sum_cost', sum_cost)

solve('13_sample.txt')	# 480
solve('13_input.txt')	# 36838

solve('13_sample.txt', offset = 10000000000000)	# 875318608908
solve('13_input.txt', offset = 10000000000000)	# 83029436920891
