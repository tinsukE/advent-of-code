# https://adventofcode.com/2023/day/21

def parse_input(filename):
	file = open(filename, 'r')
	grid = tuple([line.strip() for line in file.readlines()])
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

def calculate_filling(grid, start, steps):
	current_steps = {start}
	visited = {start}
	even_plots, odd_plots = 1, 0
	step = 0
	steps_to_fill = None
	while True if steps < 0 else step < steps:
		next_steps = set()
		while current_steps:
			pos = current_steps.pop()
			for neighbor in calculate_neighbors(grid, pos):
				if grid[neighbor[0]][neighbor[1]] != '#' and neighbor not in visited:
					visited.add(neighbor)
					next_steps.add(neighbor)
					if (abs(neighbor[0] - start[0]) + abs(neighbor[1] - start[1])) % 2 == 0:
						even_plots += 1
					else:
						odd_plots += 1
		if len(next_steps) == 0:
			steps_to_fill = step
			break
		current_steps = next_steps
		step += 1

	return ((even_plots, odd_plots), steps_to_fill)

def calculate_cardinal(grid, steps):
	length = len(grid)
	if steps <= length // 2:
		return 0

	cardinal_count = 1 + (steps - (length + 1) // 2) // length

	left_start = (length // 2, length - 1)
	left_fill, left_steps_to_fill = calculate_filling(grid, left_start, -1)

	right_start = (length // 2, 0)
	right_fill, right_steps_to_fill = calculate_filling(grid, right_start, -1)

	up_start = (length - 1, length // 2)
	up_fill, up_steps_to_fill = calculate_filling(grid, up_start, -1)

	down_start = (0, length // 2)
	down_fill, down_steps_to_fill = calculate_filling(grid, down_start, -1)

	sum_plots = 0
	for i in range(cardinal_count):
		steps_to_reach = length // 2 + 1 + length * i

		if steps - steps_to_reach > left_steps_to_fill:
			sum_plots += left_fill[(steps + i) % 2]
		else:
			if DEBUG: print('horizontal steps', steps - steps_to_reach)
			if DEBUG: print('left filling', calculate_filling(grid, left_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, left_start, steps - steps_to_reach)[0][(steps + i) % 2]

		if steps - steps_to_reach > right_steps_to_fill:
			sum_plots += right_fill[(steps + i) % 2]
		else:
			if DEBUG: print('right filling', calculate_filling(grid, right_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, right_start, steps - steps_to_reach)[0][(steps + i) % 2]

		if steps - steps_to_reach > up_steps_to_fill:
			sum_plots += up_fill[(steps + i) % 2]
		else:
			if DEBUG: print('vertical steps', steps - steps_to_reach)
			if DEBUG: print('up filling', calculate_filling(grid, up_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, up_start, steps - steps_to_reach)[0][(steps + i) % 2]

		if steps - steps_to_reach > down_steps_to_fill:
			sum_plots += down_fill[(steps + i) % 2]
		else:
			if DEBUG: print('down filling', calculate_filling(grid, down_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, down_start, steps - steps_to_reach)[0][(steps + i) % 2]
	return sum_plots

def calculate_diagonal(grid, steps):
	length = len(grid)
	steps_to_reach_first = length // 2 + length // 2 + 2
	if steps < steps_to_reach_first:
		return 0

	diagonal_count = 1 + (steps - steps_to_reach_first) // length

	top_right_start = (length - 1, 0)
	top_right_fill, top_right_steps_to_fill = calculate_filling(grid, top_right_start, -1)

	bottom_right_start = (0, 0)
	bottom_right_fill, bottom_right_steps_to_fill = calculate_filling(grid, bottom_right_start, -1)

	bottom_left_start = (0, length - 1)
	bottom_left_fill, bottom_left_steps_to_fill = calculate_filling(grid, bottom_left_start, -1)

	top_left_start = (length - 1, length - 1)
	top_left_fill, top_left_steps_to_fill = calculate_filling(grid, top_left_start, -1)

	sum_plots = 0
	for i in range(diagonal_count):
		steps_to_reach = steps_to_reach_first + length * i

		if steps - steps_to_reach > top_right_steps_to_fill:
			sum_plots += top_right_fill[(steps + i) % 2] * (i + 1)
		else:
			if DEBUG: print('diagonal steps', steps - steps_to_reach)
			if DEBUG: print('top right filling', calculate_filling(grid, top_right_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, top_right_start, steps - steps_to_reach)[0][(steps + i) % 2] * (i + 1)

		if steps - steps_to_reach > bottom_right_steps_to_fill:
			sum_plots += bottom_right_fill[(steps + i) % 2] * (i + 1)
		else:
			if DEBUG: print('bottom right filling', calculate_filling(grid, bottom_right_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, bottom_right_start, steps - steps_to_reach)[0][(steps + i) % 2] * (i + 1)

		if steps - steps_to_reach > bottom_left_steps_to_fill:
			sum_plots += bottom_left_fill[(steps + i) % 2] * (i + 1)
		else:
			if DEBUG: print('bottom left filling', calculate_filling(grid, bottom_left_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, bottom_left_start, steps - steps_to_reach)[0][(steps + i) % 2] * (i + 1)

		if steps - steps_to_reach > top_left_steps_to_fill:
			sum_plots += top_left_fill[(steps + i) % 2] * (i + 1)
		else:
			if DEBUG: print('top left filling', calculate_filling(grid, top_left_start, steps - steps_to_reach))
			sum_plots += calculate_filling(grid, top_left_start, steps - steps_to_reach)[0][(steps + i) % 2] * (i + 1)
	return sum_plots

def solve(filename, steps):
	grid, start = parse_input(filename)
	if len(grid) != len(grid[0]):
		raise ValueError('rows must be equal to cols')

	if DEBUG: print(calculate_filling(grid, start, steps))
	center_plots = calculate_filling(grid, start, steps)[0][steps % 2]
	cardinal_plots = calculate_cardinal(grid, steps)
	diagonal_plots = calculate_diagonal(grid, steps)

	garden_plots = center_plots + cardinal_plots + diagonal_plots
	if DEBUG: print(center_plots, cardinal_plots, diagonal_plots)
	print(filename, 'steps', steps, 'garden_plots', garden_plots)

DEBUG = False
solve('21_sample2.txt', 6) # 36
solve('21_sample2.txt', 7) # 48
solve('21_sample2.txt', 10) # 90
solve('21_sample2.txt', 50) # 1940
solve('21_sample2.txt', 100) # 7645
solve('21_sample2.txt', 101) # 7765
solve('21_sample2.txt', 500) # 188756
solve('21_sample2.txt', 1000) # 753480
solve('21_sample2.txt', 5000) # 18807440
# ^^^ 65.5s -> 0.05s
solve('21_input.txt', 26501365) # 616583483179597
