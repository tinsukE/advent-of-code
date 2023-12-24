# https://adventofcode.com/2023/day/23

NEIGHBORS_DELTAS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def create_neighbors(grid, prev, pos, visited):
	neighbors = []
	if pos[0] > 0:
		up = (pos[0] - 1, pos[1])
		if up != prev and grid[up[0]][up[1]] != '#' and up not in visited:
			neighbors.append(up)
	if pos[0] < len(grid) - 1:
		down = (pos[0] + 1, pos[1])
		if down != prev and grid[down[0]][down[1]] != '#' and down not in visited:
			neighbors.append(down)
	if pos[1] > 0:
		left = (pos[0], pos[1] - 1)
		if left != prev and grid[left[0]][left[1]] != '#' and left not in visited:
			neighbors.append(left)
	if pos[1] < len(grid[0]) - 1:
		right = (pos[0], pos[1] + 1)
		if right != prev and grid[right[0]][right[1]] != '#' and right not in visited:
			neighbors.append(right)
	return neighbors

def is_intersection(grid, pos):
	if pos[0] == 0 or pos[0] == len(grid) - 1 or pos[1] == 0 or pos[0] == len(grid[0]) - 1:
		return True
	wall_count = 0
	if grid[pos[0] - 1][pos[1]] == '#':
		wall_count += 1
	if grid[pos[0] + 1][pos[1]] == '#':
		wall_count += 1
	if grid[pos[0]][pos[1] - 1] == '#':
		wall_count += 1
	if grid[pos[0]][pos[1] + 1] == '#':
		wall_count += 1
	return wall_count != 2

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def find_longest_path(graph, start, end):
	global DEBUG
	# item=(node, visited_nodes, steps)
	open_nodes = [(start, frozenset({start}), 0)]
	longest_path = -1
	iterations = 0
	while open_nodes:
		iterations += 1
		if iterations % 100000 == 0:
			print('iterations:', human_format(iterations), 'open_nodes:', len(open_nodes), 'longest_path:', longest_path)

		(node, visited_nodes, steps) = open_nodes.pop(-1)
		if DEBUG: print('visiting', node, visited_nodes)

		if node == end:
			path = steps + len(visited_nodes) - 1
			if path > longest_path:
				longest_path = path
				print('found a new longest_path:', longest_path)

		for (neighbor, distance) in graph[node].items():
			if neighbor in visited_nodes:
				continue

			new_visited_nodes = set(visited_nodes)
			new_visited_nodes.add(neighbor)

			open_nodes.append((neighbor, frozenset(new_visited_nodes), steps + distance))
			if DEBUG: print('queuing', neighbor, new_visited_nodes)
	return longest_path

def is_within_bounds(grid, pos):
	return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

def advance_to_intersection(grid, previous, pos):
	global NEIGHBORS_DELTAS

	steps = 1
	while True:
		tunnel = None
		for neighbor_delta in NEIGHBORS_DELTAS:
			neighbor = (pos[0] + neighbor_delta[0], pos[1] + neighbor_delta[1])
			if neighbor == previous or not is_within_bounds(grid, neighbor) or grid[neighbor[0]][neighbor[1]] == '#':
				continue

			if is_intersection(grid, neighbor):
				return (neighbor, steps)

			tunnel = neighbor
			break
		if tunnel:
			steps += 1
			previous = pos
			pos = tunnel
		else:
			raise ValueError("WTF")

def build_graph(grid, start):
	global NEIGHBORS_DELTAS

	graph = {}
	open_nodes = {start}
	while open_nodes:
		node = open_nodes.pop()
		for neighbor_delta in NEIGHBORS_DELTAS:
			neighbor = (node[0] + neighbor_delta[0], node[1] + neighbor_delta[1])
			if not is_within_bounds(grid, neighbor) or grid[neighbor[0]][neighbor[1]] == '#':
				continue

			(intersection, steps) = advance_to_intersection(grid, node, neighbor)
			graph.setdefault(node, {})[intersection] = steps
			if intersection not in graph:
				open_nodes.add(intersection)
	return graph

def solve(filename):
	global DEBUG
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	if DEBUG:
		for row in grid: print(row)

	start = (0, grid[0].index('.'))
	end = (len(grid) - 1, grid[-1].index('.'))
	if DEBUG: print('start', start, 'end', end)

	graph = build_graph(grid, start)
	if DEBUG:
		for node, connections in graph.items(): print(node, '->', connections)

	longest_path = find_longest_path(graph, start, end)
	print(filename, 'longest non-slippery path steps', longest_path)

DEBUG = False
solve('23_sample.txt') # 154
solve('23_input.txt') # 6343 < 6407 < ?
