# https://adventofcode.com/2024/day/11

import bisect

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	start = None
	end = None
	for i, line in enumerate(lines):
		if 'S' in line:
			start = (i, line.index('S'))
		if 'E' in line:
			end = (i, line.index('E'))
	return [line.strip() for line in lines], start, end

def print_area(area):
	for line in area:
		for char in line:
			print(char, end='')
		print()

def is_within_bounds(grid, pos):
	return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

MOVES = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

def solve(filename):
	area, start, end = parse_input(filename)
	print_area(area)
	print('start:', start, '| end:', end)

	node = (start, '>')
	node_costs = { node: 0 }
	nodes = []
	while node[0] != end:
		pos = node[0]
		direction = node[1]
		move = MOVES[direction]
		cost = node_costs[node]
		for new_direction, new_move in MOVES.items():
			new_pos = (pos[0] + new_move[0], pos[1] + new_move[1])
			if not is_within_bounds(area, new_pos) or area[new_pos[0]][new_pos[1]] == '#':
				continue

			new_cost = None
			if move == new_move:
				new_cost = cost + 1
			elif move[0] == new_move[0] or move[1] == new_move[1]:
				new_cost = cost + 2000 + 1
			else:
				new_cost = cost + 1000 + 1

			new_node = (new_pos, new_direction)
			current_cost = node_costs.get(new_node)
			if current_cost is None or new_cost < current_cost:
				node_costs[new_node] = new_cost

				if new_node in nodes: nodes.remove(new_node)
				bisect.insort(nodes, new_node, key=lambda n: node_costs[n])
		node = nodes.pop(0)
		
	print(node, node_costs[node])

solve('16_sample1.txt') # 7036
solve('16_sample2.txt') # 11048
solve('16_input.txt') # 134588
