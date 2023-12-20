# https://adventofcode.com/2023/day/17

def calculate_neighbors(grid, point):
	neighbors = {}
	if point[0] > 0:
		neighbors['U'] = (point[0] - 1, point[1])
	if point[0] < len(grid) - 1:
		neighbors['D'] = (point[0] + 1, point[1])
	if point[1] > 0:
		neighbors['L'] = (point[0], point[1] - 1)
	if point[1] < len(grid[0]) - 1:
		neighbors['R'] = (point[0], point[1] + 1)
	return neighbors

def position_diff(a, b):
	return (a[0] - b[0], a[1] - b[1])

def my_star(grid, start, end):
	INFINITY = float('inf')

	open_set = {start}
	came_from = {}

	cost_map = {}
	cost_map[start] = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'C': 0}

	while open_set:
		current = min(open_set, key=lambda pos: cost_map[pos]['C'])
		print('current', current, 'cost', cost_map[current])
		if current == end:
			print('found!')
			return cost_map[current]['C']

		open_set.remove(current)
		for direction, neighbor in calculate_neighbors(grid, current).items():
			current_movement = cost_map[current][direction]
			current_cost = cost_map[current]['C']
			if current_movement == 3:
				continue

			print('evaluating neighbor', neighbor)
			neighbor_cost = current_cost + grid[neighbor[0]][neighbor[1]]
			if neighbor not in cost_map:
				print('first neighbor!')
				cost_map[neighbor] = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'C': neighbor_cost}
				cost_map[neighbor][direction] = current_movement + 1
			elif neighbor_cost < cost_map[neighbor]['C']:
				print('best neighbor!')
				cost_map[neighbor] = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'C': neighbor_cost}
				cost_map[neighbor][direction] = current_movement + 1
			elif neighbor_cost == cost_map[neighbor]['C']:
				print('existing neighbor!')
				if any(key != 'C' and key != direction and cost_map[neighbor][key] > 0 for key in cost_map[neighbor]):
					cost_map[neighbor] = {'U': 0, 'D': 0, 'L': 0, 'R': 0, 'C': neighbor_cost}
				elif cost_map[neighbor][direction] < current_movement + 1:
					cost_map[neighbor][direction] = current_movement + 1
				# else:
				# 	print('bad existing neighbor...')
				# 	continue
			else:
				print('bad neighbor... cost', neighbor_cost, 'previously', cost_map[neighbor])
				continue
			if neighbor not in open_set:
				open_set.add(neighbor)

	print('oops...')
	return None

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]
	for row in grid: print(row)

	heat_loss = my_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1))
	print(filename, 'heat_loss', heat_loss)

solve_1('17_sample.txt')