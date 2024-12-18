# https://adventofcode.com/2024/day/18

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	return [(int(n[0]), int(n[1])) for n in [line.strip().split(',') for line in lines]]

def empty_grid(dim):
	return [['.' for _ in range(dim)] for _ in range(dim)]

def add_byte(grid, pos):
	grid[pos[1]][pos[0]] = '#'

def print_grid(grid):
	for line in grid:
		for char in line:
			print(char, end='')
		print()

DELTAS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
def neighbors(pos):
	return [(pos[0] + delta[0], pos[1] + delta[1]) for delta in DELTAS]

def is_within_bounds(grid, pos):
	return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

def steps_to_end(grid):
	start = (0, 0)
	end = (len(grid) - 1, len(grid) - 1)

	costs = {start: 0}
	start_visited = set()
	start_visited.add(start)
	visited = {start: start_visited}
	to_visit = []
	node = start

	while node != end:
		cost = costs[node]
		for neighbor in neighbors(node):
			if not is_within_bounds(grid, neighbor):
				continue
			if neighbor in visited:
				continue
			if grid[neighbor[0]][neighbor[1]] == '#':
				continue
			neighbor_visited = set(visited[node])
			neighbor_visited.add(neighbor)
			visited[neighbor] = neighbor_visited
			to_visit.append(neighbor)
			costs[neighbor] = cost + 1

		if len(to_visit) == 0:
			break
		node = to_visit.pop(0)

	return (costs.get(end, None), visited.get(end, None))

def solve_1(filename, dim, nanos):
	incoming_bytes = parse_input(filename)
	grid = empty_grid(dim)
	for incoming in incoming_bytes[0:nanos]:
		add_byte(grid, incoming)
	# print_grid(grid)

	print('steps', steps_to_end(grid)[0])

def solve_2(filename, dim):
	incoming_bytes = parse_input(filename)
	grid = empty_grid(dim)
	visited = None

	for incoming in incoming_bytes:
		add_byte(grid, incoming)
		# only re-check if there is a solution if the byte
		# is falling on the path of the current one
		if visited and (incoming[1], incoming[0]) not in visited:
			continue
		(cost, visited) = steps_to_end(grid)
		if cost is None:
			print('final byte', incoming)
			return
	print('fudge')

solve_1('18_sample.txt', 7, 12)	# 22
solve_1('18_input.txt', 71, 1024) # 298

solve_2('18_sample.txt', 7) # 6,1
solve_2('18_input.txt', 71) # 52,32
