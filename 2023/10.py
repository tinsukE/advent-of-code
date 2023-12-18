# https://adventofcode.com/2023/day/10

def build_input(filename):
	file = open(filename, 'r')
	maze = [[*line.strip()] for line in file.readlines()]
	start_i = next((i for i, row in enumerate(maze) if 'S' in row))
	start_j = maze[start_i].index('S')
	return ((start_i, start_j), maze)

def connects_up(maze, pos):
	try: return maze[pos[0]][pos[1]] in ('S', '|', 'L', 'J')
	except: return false

def connects_down(maze, pos):
	try: return maze[pos[0]][pos[1]] in ('S', '|', 'F', '7')
	except: return false

def connects_left(maze, pos):
	try: return maze[pos[0]][pos[1]] in ('S', '-', 'J', '7')
	except: return false

def connects_right(maze, pos):
	try: return maze[pos[0]][pos[1]] in ('S', '-', 'F', 'L')
	except: return false

def find_connections(pos, prev_pos, maze):
	connections = []
	up = (pos[0] - 1, pos[1])
	if prev_pos != up and connects_up(maze, pos) and connects_down(maze, up):
		connections.append(up)
	down = (pos[0] + 1, pos[1])
	if prev_pos != down and connects_down(maze, pos) and connects_up(maze, down):
		connections.append(down)
	left = (pos[0], pos[1] - 1)
	if prev_pos != left and connects_left(maze, pos) and connects_right(maze, left):
		connections.append(left)
	right = (pos[0], pos[1] + 1)
	if prev_pos != right and connects_right(maze, pos) and connects_left(maze, right):
		connections.append(right)
	return connections

def solve_1(filename):
	(start, maze) = build_input(filename)

	steps = 1
	positions = find_connections(start, None, maze)
	old_positions = [start, start]

	while positions[0] == start or positions[0] != positions[1]:
		steps += 1
		new_positions = [
			find_connections(positions[0], old_positions[0], maze)[0],
			find_connections(positions[1], old_positions[1], maze)[0]
		]
		old_positions = positions
		positions = new_positions
	print(filename, "part 1 steps:", steps)

def count_barriers(maze, positions, barriers, mod_barriers):
	num_barriers = 0
	num_mod_barriers = 0
	for pos in positions:
		if maze[pos[0]][pos[1]] in barriers:
			num_barriers += 1
		elif maze[pos[0]][pos[1]] in mod_barriers:
			num_mod_barriers += 1
	return num_barriers + (num_mod_barriers % 2)

def is_inside_loop(maze, row, col):
	left = count_barriers(maze, list(map(lambda j: (row, j), range(0, col))), '|', 'LJ')
	up = count_barriers(maze, list(map(lambda i: (i, col), range(0, row))), '-', 'FL')

	return left % 2 == 1 or up % 2 == 1

def determine_start(maze, start, positions):
	deltas = [(pos[0] - start[0], pos[1] - start[1]) for pos in positions]
	if (0, 1) in deltas and (0, -1) in deltas:
		maze[start[0]][start[1]] = '-'
	elif (1, 0) in deltas and (-1, 0) in deltas:
		maze[start[0]][start[1]] = '|'
	elif (0, 1) in deltas and (1, 0) in deltas:
		maze[start[0]][start[1]] = 'F'
	elif (0, -1) in deltas and (1, 0) in deltas:
		maze[start[0]][start[1]] = '7'
	elif (0, 1) in deltas and (-1, 0) in deltas:
		maze[start[0]][start[1]] = 'L'
	else:
		maze[start[0]][start[1]] = 'J'

def copy_position(src, dst, pos):
	dst[pos[0]][pos[1]] = src[pos[0]][pos[1]]

def solve_2(filename):
	(start, maze) = build_input(filename)
	simple_maze = [['.' for col in row] for row in maze]

	positions = find_connections(start, None, maze)
	determine_start(simple_maze, start, positions)
	copy_position(maze, simple_maze, positions[0])
	copy_position(maze, simple_maze, positions[1])
	old_positions = [start, start]

	while positions[0] == start or positions[0] != positions[1]:
		new_positions = [
			find_connections(positions[0], old_positions[0], maze)[0],
			find_connections(positions[1], old_positions[1], maze)[0]
		]
		old_positions = positions
		positions = new_positions
		copy_position(maze, simple_maze, positions[0])
		copy_position(maze, simple_maze, positions[1])

	sum_inside = 0
	for i in range(len(simple_maze)):
		for j in range(len(simple_maze[i])):
			char = simple_maze[i][j]
			if char != '.':
				continue
			if is_inside_loop(simple_maze, i, j):
				simple_maze[i][j] = 'I'
				sum_inside += 1
			else:
				simple_maze[i][j] = 'O'

	print(filename, "part 2 inside:", sum_inside)

solve_1('10_sample1.txt')
solve_1('10_sample2.txt')
solve_1('10_input.txt')

solve_2('10_sample3.txt')
solve_2('10_sample4.txt')
solve_2('10_input.txt')
