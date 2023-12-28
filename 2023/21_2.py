# https://adventofcode.com/2023/day/21

def parse_input(filename):
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	if DEBUG:
		for row in grid: print(row)
	start = None
	for i, row in enumerate(grid):
		for j, item in enumerate(row):
			if item == 'S':
				start = (i, j)
				break
		if start:
			break
	if DEBUG:
		print(start)
	return (grid, start)

def calculate_neighbors_infinite(grid, pos):
	neighbors = []
	neighbors.append((pos[0] - 1, pos[1]))
	neighbors.append((pos[0] + 1, pos[1]))
	neighbors.append((pos[0], pos[1] - 1))
	neighbors.append((pos[0], pos[1] + 1))
	return neighbors

def solve_2(filename, steps):
	grid, start = parse_input(filename)
	rows = len(grid)
	cols = len(grid[0])

	visited = set()

	current_steps = {start}
	for step in range(1, steps + 1):
		if step % 1000 == 0:
			print('processing step', step, 'visited', len(visited))
		next_steps = set()
		while current_steps:
			pos = current_steps.pop()
			for neighbor in calculate_neighbors_infinite(grid, pos):
				if grid[neighbor[0] % rows][neighbor[1] % cols] != '#':
					visit = (step % 2, neighbor)
					if visit not in visited:
						visited.add(visit)
						next_steps.add(neighbor)
		current_steps = next_steps

	plots = sum(1 for visit in visited if visit[0] == steps % 2)

	print(filename, 'steps', steps, 'infinite garden plots', plots)

DEBUG = False
solve_2('21_sample2.txt', 6) # 36
solve_2('21_sample2.txt', 7) # 48
solve_2('21_sample2.txt', 10) # 90
solve_2('21_sample2.txt', 50) # 1940
solve_2('21_sample2.txt', 100) # 7645
solve_2('21_sample2.txt', 101) # 7765
solve_2('21_sample2.txt', 500) # 188756
solve_2('21_sample2.txt', 1000) # 753480
solve_2('21_sample2.txt', 5000) # 18807440
# ^^^ 65.5s
# solve_2('21_input.txt', 26501365) # ???
