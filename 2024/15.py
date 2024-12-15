# https://adventofcode.com/2024/day/15

import math

def parse_input(filename):
	file = open(filename, 'r')
	warehouse = []
	robot = None
	line = file.readline().strip()
	while len(line) > 0:
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
def move_robot(warehouse, robot, move):
	move_delta = MOVES[move]
	# print('Move', move, move_delta)
	pos = (robot[0] + move_delta[0], robot[1] + move_delta[1])
	while is_within_bounds(warehouse, pos) and warehouse[pos[0]][pos[1]] == 'O':
		pos = (pos[0] + move_delta[0], pos[1] + move_delta[1])

	new_robot = robot
	if is_within_bounds(warehouse, pos) and warehouse[pos[0]][pos[1]] == '.':
		new_robot = (robot[0] + move_delta[0], robot[1] + move_delta[1])
		warehouse[new_robot[0]][new_robot[1]] = '@'
		warehouse[robot[0]][robot[1]] = '.'

		while pos != new_robot:
			warehouse[pos[0]][pos[1]] = 'O'
			pos = (pos[0] - move_delta[0], pos[1] - move_delta[1])

	return new_robot

def solve(filename):
	warehouse, robot, moves = parse_input(filename)

	for move in moves:
		robot = move_robot(warehouse, robot, move)
		# print_warehouse(warehouse)
		# print(robot)

	gps_sum = 0
	for i, line in enumerate(warehouse):
		for j, char in enumerate(line):
			if char == 'O':
				gps_sum += i * 100 + j
	print('gps_sum', gps_sum)

solve('15_sample1.txt')	# 2028
solve('15_sample2.txt') # 10092
solve('15_input.txt') # 10092
