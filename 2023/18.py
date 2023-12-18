# https://adventofcode.com/2023/day/18

def track_boundary(boundaries, position):
	boundary = boundaries.get(position[1], (None, None))
	if position[1] == 5:
		print(position, boundary)
	if boundary[0] == None or position[0] < boundary[0]:
		if position[1] == 5:
			if not boundary[0]:
				print('init')
			else:
				print(position[0] < boundary[0])
			print('changing lower to', position[0])
		boundary = (position[0], boundary[1])
	if boundary[1] == None or position[0] > boundary[1]:
		if position[1] == 5:
			print('changing upper to', position[0])
		boundary = (boundary[0], position[0])
	boundaries[position[1]] = boundary

def solve_1(filename):
	file = open(filename, 'r')

	min_row = 0
	max_row = 0
	boundaries = { 0: (0, 0) }

	position = (0, 0)
	for line in [line.strip() for line in file.readlines()]:
		(direction, distance, _) = line.split()
		distance = int(distance)
		print(direction, distance)
		if direction == 'U':
			for y in range(position[1] - distance, position[1]):
				track_boundary(boundaries, (position[0], y))
			position = (position[0], position[1] - distance)
		elif direction == 'D':
			for y in range(position[1], position[1] + distance + 1):
				track_boundary(boundaries, (position[0], y))
			position = (position[0], position[1] + distance)
		elif direction == 'L':
			for x in range(position[0] - distance, position[0]):
				track_boundary(boundaries, (x, position[1]))
			position = (position[0] - distance, position[1])
		elif direction == 'R':
			for x in range(position[0], position[0] + distance + 1):
				track_boundary(boundaries, (x, position[1]))
			position = (position[0] + distance, position[1])
	print(boundaries)

	lava_volume = 0
	print(len(boundaries), sorted(boundaries.keys()))
	for boundary in boundaries.values():
		lava_volume += boundary[1] - boundary[0] + 1
	print(filename, 'lava_volume', lava_volume)

solve_1('18_sample.txt')
# solve_1('18_input.txt')
