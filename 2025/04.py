# https://adventofcode.com/2025/day/4

def parse_input(filename):
	file = open(filename, 'r')
	grid = []
	for line in [line.strip() for line in file.readlines()]:
		grid.append(list(line))
	return grid

def element_at(grid, row, col):
	if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
		return None
	return grid[row][col]

def count_adjacent_rolls(grid, row, col):
	adjacent_rolls = 0

	adjacent = [
		(row-1, col-1), (row-1, col), (row-1,col+1),
		(row, col-1), 				  (row,col+1),
		(row+1, col-1), (row+1, col), (row+1,col+1)
	]

	return sum(1 for pos in adjacent if element_at(grid, pos[0], pos[1]) == '@')

def solve_1(filename):
	grid = parse_input(filename)

	accessible_rolls = 0

	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if grid[row][col] == '@' and count_adjacent_rolls(grid, row, col) < 4:
				accessible_rolls += 1

	print("accessible_rolls", accessible_rolls)

def solve_2(filename):
	grid = parse_input(filename)

	removed_rolls = 0

	while True:
		removed = False
		for row in range(len(grid)):
			for col in range(len(grid[0])):
				if grid[row][col] == '@' and count_adjacent_rolls(grid, row, col) < 4:
					grid[row][col] = '.'
					removed_rolls += 1
					removed = True
		if not removed:
			break

	print("removed_rolls", removed_rolls)

solve_1('04_sample.txt') # 13
solve_1('04_input.txt') # 1437

solve_2('04_sample.txt') # 43
solve_2('04_input.txt') # 8765
