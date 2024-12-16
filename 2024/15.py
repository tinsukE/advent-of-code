# https://adventofcode.com/2024/day/15

def parse_input(filename, expand = False):
	file = open(filename, 'r')
	warehouse = []
	robot = None
	line = file.readline().strip()
	while len(line) > 0:
		if expand:
			row = []
			for char in line:
				if char == '#':
					row.extend(['#', '#'])
				elif char == 'O':
					row.extend(['[', ']'])
				elif char == '.':
					row.extend(['.', '.'])
				elif char == '@':
					robot = (len(warehouse), len(row))
					row.extend(['@', '.'])
				else:
					raise ValueError('Unexpected character', char)
			warehouse.append(row)
		else:
			if '@' in line:
				robot = (len(warehouse), line.index('@'))
			warehouse.append([char for char in line])
		line = file.readline().strip()
	moves = []
	line = file.readline().strip()
	while line:
		moves.extend(line)
		line = file.readline().strip()
	return warehouse, robot, moves

def print_warehouse(warehouse):
	for line in warehouse:
		for char in line:
			print(char, end='')
		print()

def is_within_bounds(grid, pos):
	return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

MOVES = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
def move_items(warehouse, move, items):
	if len(items) == 0:
		return []

	delta = MOVES[move]
	moved_items = [(item[0] + delta[0], item[1] + delta[1]) for item in items]
	items_to_move = set()

	for moved_item in moved_items:
		if not is_within_bounds(warehouse, moved_item):
			return None
		
		value = warehouse[moved_item[0]][moved_item[1]]
		if value == '#':
			return None

		if value == 'O' or value == '[' or value == ']':
			items_to_move.add(moved_item)
			if move == '^' or move == 'v':
				if value == '[':
					items_to_move.add((moved_item[0], moved_item[1] + 1))
				elif value == ']':
					items_to_move.add((moved_item[0], moved_item[1] - 1))

	if move_items(warehouse, move, list(items_to_move)) == None:
		return None

	for (item, moved_item) in zip(items, moved_items):
		warehouse[moved_item[0]][moved_item[1]] = warehouse[item[0]][item[1]]
		warehouse[item[0]][item[1]] = '.'

	return moved_items

def calculate_gps_sum(warehouse, item):
	gps_sum = 0
	for i, line in enumerate(warehouse):
		for j, char in enumerate(line):
			if char == item:
				gps_sum += i * 100 + j
	return gps_sum

def solve(filename):
	warehouse, robot, moves = parse_input(filename)
	# print_warehouse(warehouse)

	for move in moves:
		# print('\nMove', move)
		moved_robot = move_items(warehouse, move, [robot])
		robot = moved_robot[0] if moved_robot is not None else robot
		# print_warehouse(warehouse)
		# print(robot)

	print('gps_sum', calculate_gps_sum(warehouse, 'O'))

def solve_2(filename):
	warehouse, robot, moves = parse_input(filename, expand = True)
	# print_warehouse(warehouse)

	for move in moves:
		# print('\nMove', move)
		moved_robot = move_items(warehouse, move, [robot])
		robot = moved_robot[0] if moved_robot is not None else robot
		# print_warehouse(warehouse)
		# print(robot)

	print('gps_sum', calculate_gps_sum(warehouse, '['))

solve('15_sample1.txt')	# 2028
solve('15_sample2.txt') # 10092
solve('15_input.txt') # 1495147

solve_2('15_sample3.txt') # 618
solve_2('15_sample2.txt') # 9021
solve_2('15_input.txt') # 1524905
