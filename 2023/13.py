# https://adventofcode.com/2023/day/13

def build_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	breaks = [i for i in range(len(lines)) if len(lines[i]) == 0]
	breaks.insert(0, -1)
	breaks.append(len(lines))

	return [lines[breaks[i] + 1:breaks[i + 1]] for i in range(len(breaks) - 1)]

def row_diff(terrain, row1, row2):
	diff = 0
	for col in range(len(terrain[0])):
		if terrain[row1][col] != terrain[row2][col]:
			diff += 1
	return diff

def col_diff(terrain, col1, col2):
	diff = 0
	for row in range(len(terrain)):
		if terrain[row][col1] != terrain[row][col2]:
			diff += 1
	return diff

def find_horizontal_split(terrain, diff):
	for split in range(len(terrain) - 1):
		delta_row = min(split + 1, len(terrain) - split - 1)

		actual_diff = 0
		for i in range(delta_row):
			actual_diff += row_diff(terrain, split - i, split + i + 1)
		if actual_diff == diff:
			return split
	return -1

def find_vertical_split(terrain, diff):
	cols = len(terrain[0])
	for split in range(cols - 1):
		delta_col = min(split + 1, cols - split - 1)

		actual_diff = 0
		for j in range(delta_col):
			actual_diff += col_diff(terrain, split - j, split + j + 1)
		if actual_diff == diff:
			return split
	return -1

def solve(filename, diff = 0):
	terrains = build_input(filename)

	sum_splits = 0
	for terrain in terrains:
		horizontal = find_horizontal_split(terrain, diff)
		if horizontal != -1:
			sum_splits += (horizontal + 1) * 100
			continue
		vertical = find_vertical_split(terrain, diff)
		if vertical != -1:
			sum_splits += vertical + 1
	print(filename, 'part 1:', sum_splits)

solve('13_sample.txt')
solve('13_input.txt')

solve('13_sample.txt', 1)
solve('13_input.txt', 1)
