# https://adventofcode.com/2023/day/23

def create_neighbors(grid, pos):
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

def find_longest_path(grid, start, end, slippery_slope):
	global DEBUG
	open_nodes = [(start, {start})]
	longest_path = set()
	iterations = 0
	while open_nodes:
		iterations += 1
		if iterations % 100000 == 0:
			print('iterations:', human_format(iterations), 'open_nodes:', len(open_nodes), 'longest_path:', len(longest_path) if longest_path else None)
		# node = max(open_nodes, key=lambda node: len(node[1]))
		node = open_nodes.pop(-1)
		(head, visited_nodes) = node
		if DEBUG: print('visiting', head, visited_nodes)
		# open_nodes.remove(node)

		if head == end:
			if longest_path == None or len(visited_nodes) > len(longest_path):
				longest_path = visited_nodes
				print('found a new longest_path:', len(longest_path))

		for neighbor in create_neighbors(grid, head):
			if grid[neighbor[0]][neighbor[1]] == '#' or neighbor in visited_nodes:
				continue
			new_visited_nodes = set(visited_nodes)
			new_visited_nodes.add(neighbor)

			if slippery_slope:
				while grid[neighbor[0]][neighbor[1]] != '.':
					if grid[neighbor[0]][neighbor[1]] == '^':
						neighbor = (neighbor[0] - 1, neighbor[1])
					elif grid[neighbor[0]][neighbor[1]] == 'v':
						neighbor = (neighbor[0] + 1, neighbor[1])
					elif grid[neighbor[0]][neighbor[1]] == '<':
						neighbor = (neighbor[0], neighbor[1] - 1)
					elif grid[neighbor[0]][neighbor[1]] == '>':
						neighbor = (neighbor[0], neighbor[1] + 1)
					else:
						raise ValueError('Oops...')
					new_visited_nodes.add(neighbor)
				if neighbor in visited_nodes:
					if DEBUG: print('Got a slider!!!')
					continue

			open_nodes.append((neighbor, new_visited_nodes))
			if DEBUG: print('queuing', neighbor, new_visited_nodes)
	return longest_path

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def solve(filename, slippery_slope):
	global DEBUG
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	if DEBUG:
		for row in grid: print(row)

	start = (0, grid[0].index('.'))
	end = (len(grid) - 1, grid[-1].index('.'))
	if DEBUG: print('start', start, 'end', end)

	longest_path = find_longest_path(grid, start, end, slippery_slope)
	print(filename, 'longest', 'slippery' if slippery_slope else '', 'path steps', len(longest_path) - 1)

DEBUG = False
# solve('23_sample.txt', slippery_slope=True)
# solve('23_input.txt', slippery_slope=True)

# solve('23_sample.txt', slippery_slope=False)
solve('23_input.txt', slippery_slope=False)
