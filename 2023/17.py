# https://adventofcode.com/2023/day/17

def distance_heuristic(grid, point, end):
	return abs(point[0] - end[0]) * abs(point[1] - end[1])

def reconstruct_path(came_from, current):
	total_path = [current]
	while current in came_from:
		current = came_from[current]
		total_path.insert(0, current)
	return total_path

def calculate_neighbors(grid, point):
	neighbors = []
	if point[0] > 0:
		neighbors.append((point[0] - 1, point[1]))
	if point[0] < len(grid) - 1:
		neighbors.append((point[0] + 1, point[1]))
	if point[1] > 0:
		neighbors.append((point[0], point[1] - 1))
	if point[1] < len(grid[0]) - 1:
		neighbors.append((point[0], point[1] + 1))
	return neighbors

def position_diff(a, b):
	return (a[0] - b[0], a[1] - b[1])

def a_star(grid, start, end):
	open_set = {start}
	came_from = {}

	g_score = {}
	g_score[start] = 0

	f_score = {}
	f_score[start] = 0 #distance_heuristic(grid, start, end)

	while open_set:
		current = min(open_set, key = lambda pos: f_score.get(pos, 999999999))
		if current == end:
			print('found!')
			print(g_score)
			return reconstruct_path(came_from, current)

		open_set.remove(current)
		for neighbor in calculate_neighbors(grid, current):
			direction = position_diff(neighbor, current)
			# previous = came_from.get(current)
			# if previous and direction == position_diff(current, previous):
			# 	pre_previous = came_from.get(previous)
			# 	if pre_previous and direction == position_diff(previous, pre_previous):
			# 		continue

			tentative_gscore = g_score[current] + grid[neighbor[0]][neighbor[1]]
			if tentative_gscore < g_score.get(neighbor, 999999999):
				came_from[neighbor] = current
				g_score[neighbor] = tentative_gscore
				f_score[neighbor] = tentative_gscore # + distance_heuristic(grid, neighbor, end)
				if neighbor not in open_set:
					open_set.add(neighbor)

	print('oops...')
	return None

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[int(char) for char in line.strip()] for line in file.readlines()]
	for row in grid: print(row)

	path = a_star(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1))
	print(path)
	heat_loss = sum([grid[pos[0]][pos[1]] for pos in path[1:]])
	print(filename, 'heat_loss', heat_loss)

solve_1('17_sample.txt')