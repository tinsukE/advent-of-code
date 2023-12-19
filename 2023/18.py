# https://adventofcode.com/2023/day/18

from functools import reduce
from itertools import pairwise

# How do I calculate the area of a 2d polygon?
# https://stackoverflow.com/a/451482/477243
def area(p):
	return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p)))
def segments(p):
	return zip(p, p[1:] + [p[0]])

def perimeter(points):
	return reduce(lambda sum, p: sum + abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1]), pairwise(points), 0)

def solve(filename, instruction_builder):
	file = open(filename, 'r')

	position = (0, 0)
	points = [position]

	for line in [line.strip() for line in file.readlines()]:
		(direction, distance) = instruction_builder(line)
		if direction == 'U':
			position = (position[0] - distance, position[1])
		elif direction == 'D':
			position = (position[0] + distance, position[1])
		elif direction == 'L':
			position = (position[0], position[1] - distance)
		elif direction == 'R':
			position = (position[0], position[1] + distance)
		points.append(position)

	return area(points) + perimeter(points) / 2 + 1

def solve_1(filename):
	def parse_line(line):
		(direction, distance, _) = line.split()
		distance = int(distance)
		return (direction, distance)
	print(filename, 'volume 1', solve(filename, parse_line))

def solve_2(filename):
	def parse_line(line):
		(_, _, hexa) = line.split()
		distance = hexa[2:7]
		distance = int(hexa[2:7], 16)
		direction = hexa[7]
		if direction == '0':
			direction = 'R'
		elif direction == '1':
			direction = 'D'
		elif direction 	== '2':
			direction = 'L'
		elif direction 	== '3':
			direction = 'U'
		return (direction, distance)
	print(filename, 'volume 2', solve(filename, parse_line))


solve_1('18_sample.txt')
solve_1('18_input.txt')

solve_2('18_sample.txt')
solve_2('18_input.txt')
