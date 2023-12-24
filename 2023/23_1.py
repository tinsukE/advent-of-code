# https://adventofcode.com/2023/day/23

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

def find_longest_path(grid, start, end):
	global DEBUG
	# item=(previous, position, visited_intersections, steps)
	open_nodes = [(None, start, {start}, 0)]
	longest_path = -1
	iterations = 0
	while open_nodes:
		iterations += 1
		if iterations % 10000 == 0:
			print('iterations:', human_format(iterations), 'open_nodes:', len(open_nodes), 'longest_path:', longest_path)

		node = open_nodes.pop(-1)
		(previous, position, visited_intersections, steps) = node
		if DEBUG: print('visiting', position, visited_intersections)

		if position == end:
			if steps > longest_path:
				longest_path = steps
				print('found a new longest_path:', longest_path)

		neighbors = create_neighbors(grid, previous, position, visited_intersections)
		if len(neighbors) > 1:
			visited_intersections = set(visited_intersections)
			visited_intersections.add(position)

		for neighbor in neighbors:
			steps_increment = 1
			neighbor_previous = position
			while grid[neighbor[0]][neighbor[1]] != '.':
				neighbor_previous = neighbor
				steps_increment += 1
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
			if neighbor == previous or neighbor in visited_intersections:
				if DEBUG: print('Got a slider!!!')
				continue

			open_nodes.append((neighbor_previous, neighbor, visited_intersections, steps + steps_increment))
			if DEBUG: print('queuing', neighbor, visited_intersections)
	return longest_path

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def solve(filename):
	global DEBUG
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	if DEBUG:
		for row in grid: print(row)

	start = (0, grid[0].index('.'))
	end = (len(grid) - 1, grid[-1].index('.'))
	if DEBUG: print('start', start, 'end', end)

	longest_path = find_longest_path(grid, start, end)
	print(filename, 'longest slippery path steps', longest_path)

DEBUG = False
solve('23_sample.txt') # 94
solve('23_input.txt') # 2094
