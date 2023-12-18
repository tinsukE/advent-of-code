# https://adventofcode.com/2023/day/18

from numpy import tile

def determine_connection(curr, prev, after):
	if curr[0] - prev[0] > 0 and after[1] - curr[1] > 0 or curr[1] - prev[1] < 0 and after[0] - curr[0] < 0:
		return 'L'
	if curr[0] - prev[0] > 0 and after[1] - curr[1] < 0 or curr[1] - prev[1] > 0 and after[0] - curr[0] < 0:
		return 'J'
	if curr[0] - prev[0] < 0 and after[1] - curr[1] > 0 or curr[1] - prev[1] < 0 and after[0] - curr[0] > 0:
		return 'F'
	if curr[0] - prev[0] < 0 and after[1] - curr[1] < 0 or curr[1] - prev[1] > 0 and after[0] - curr[0] > 0:
		return '7'
	return '@'

def fill_connections(loop, points):
	start = points[0]
	loop[start[0]][start[1]] = determine_connection(start, points[-2], points[1])

	for i in range(1, len(points) - 1):
		point = points[i]
		loop[point[0]][point[1]] = determine_connection(point, points[i - 1], points[(i + 1) % len(points)])

def build_loop(points):
	top_left = (min(points, key=lambda p: p[0])[0], min(points, key=lambda p: p[1])[1])
	bottom_right = (max(points, key=lambda p: p[0])[0], max(points, key=lambda p: p[1])[1])
	print(top_left, bottom_right)

	offset = (-top_left[0], -top_left[1])
	print('offset', offset)

	rows = bottom_right[0] - top_left[0] + 1
	cols = bottom_right[1] - top_left[1] + 1

	points = [(point[0] + offset[0], point[1] + offset[1]) for point in points]

	loop = tile('.', (rows, cols))

	print('loop initialized')

	src = points[0]
	loop[src[0]][src[1]] = 'S'

	for dst in points[1:]:
		if dst[0] > src[0]:
			for row in range(src[0] + 1, dst[0]):
				loop[row][dst[1]] = '|'
		elif dst[0] < src[0]:
			for row in range(dst[0] + 1, src[0]):
				loop[row][dst[1]] = '|'
		elif dst[1] > src[1]:
			for col in range(src[1] + 1, dst[1]):
				loop[dst[0]][col] = '-'
		elif dst[1] < src[1]:
			for col in range(dst[1] + 1, src[1]):
				loop[dst[0]][col] = '-'
		src = dst

	print('straights filled')

	fill_connections(loop, points)

	print('connections filled')

	# for row in loop: print(row)
	return loop

def calculate_volume(loop):
	volume = 0
	for row in loop:
		inside = False
		for item in row:
			if item in ('|', 'L', 'J'):
				inside = not inside
			if item == '.' and inside or item != '.':
				volume += 1
	return volume

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

	# print(points)
	print('points built')
	loop = build_loop(points)
	print('loop built')
	return calculate_volume(loop)

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

# solve_2('18_sample.txt')
