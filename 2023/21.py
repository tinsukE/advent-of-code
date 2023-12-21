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

def solve_1(filename, steps):
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

# solve_1('21_sample.txt', 1)
# solve_1('21_sample.txt', 2)
# solve_1('21_sample.txt', 3)
# solve_1('21_sample.txt', 4)
# solve_1('21_sample.txt', 5)
# solve_1('21_sample.txt', 6)
# solve_1('21_input.txt', 64)

solve_2('21_sample.txt', 6)
solve_2('21_sample.txt', 10)
solve_2('21_sample.txt', 50)
solve_2('21_sample.txt', 100)
solve_2('21_sample.txt', 500)
solve_2('21_sample.txt', 1000)
solve_2('21_sample.txt', 5000)
solve_2('21_input.txt', 26501365)
