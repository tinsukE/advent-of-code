# https://adventofcode.com/2023/day/21

def parse_input(filename):
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	# for row in grid: print(row)
	start = None
	for i, row in enumerate(grid):
		for j, item in enumerate(row):
			if item == 'S':
				start = (i, j)
				break
		if start:
			break
	# print(start)
	return (grid, start)

def calculate_neighbors(grid, pos):
	neighbors = []
	if pos[0] > 0:
		neighbors.append((pos[0] - 1, pos[1]))
	if pos[0] < len(grid) - 1:
		neighbors.append((pos[0] + 1, pos[1]))
	if pos[1] > 0:
		neighbors.append((pos[0], pos[1] - 1))
	if pos[1] < len(grid[0]) - 1:
		neighbors.append((pos[0], pos[1] + 1))
	return neighbors

def solve(filename, steps):
	grid, start = parse_input(filename)

	current_steps = {start}
	for _ in range(steps):
		next_steps = set()
		while current_steps:
			pos = current_steps.pop()
			for neighbor in calculate_neighbors(grid, pos):
				if grid[neighbor[0]][neighbor[1]] != '#':
					next_steps.add(neighbor)
		current_steps = next_steps

	print(filename, 'steps', steps, 'garden plots', len(current_steps))

solve('21_sample.txt', 1) # 2
solve('21_sample.txt', 2) # 4
solve('21_sample.txt', 3) # 6
solve('21_sample.txt', 4) # 9
solve('21_sample.txt', 5) # 13
solve('21_sample.txt', 6) # 16
solve('21_input.txt', 64) # 3716
