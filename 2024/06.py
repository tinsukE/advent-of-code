# https://adventofcode.com/2024/day/6

from collections import defaultdict
from copy import deepcopy

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	for i, line in enumerate(lines):
		for j, char in enumerate(line):
			if char == '^':
				return (lines, (i, j))

	return (lines, None)

def is_within_bounds(area_map, pos):
	return pos[0] >= 0 and pos[0] < len(area_map) and pos[1] >= 0 and pos[1] < len(area_map[0])

def solve(filename):
	(area_map, original_pos) = parse_input(filename)

	pos = original_pos
	dir_index = 0
	visited_pos = set()
	tested = set()
	obstructions = 0

	while True:
		visited_pos.add(pos)

		direction = DIRECTIONS[dir_index]
		new_pos = (pos[0] + direction[0], pos[1] + direction[1])
		if not is_within_bounds(area_map, new_pos):
			break

		tile = area_map[new_pos[0]][new_pos[1]]
		if tile == "#":
			dir_index = (dir_index + 1) % len(DIRECTIONS)
		else:
			pos = new_pos

			if new_pos not in tested and has_loop(area_map, original_pos, new_pos):
				obstructions += 1
			tested.add(new_pos)

	print("len(visited_pos)", len(visited_pos))
	print("obstructions", obstructions)

def has_loop(area_map, pos, obstruction):
	dir_index = 0
	visited_pos = defaultdict(set)

	while True:
		direction = DIRECTIONS[dir_index]

		if direction in visited_pos[pos]:
			return True

		visited_pos[pos].add(direction)

		new_pos = (pos[0] + direction[0], pos[1] + direction[1])
		if not is_within_bounds(area_map, new_pos):
			break

		tile = area_map[new_pos[0]][new_pos[1]]
		if tile == "#" or new_pos == obstruction:
			dir_index = (dir_index + 1) % len(DIRECTIONS)
		else:
			pos = new_pos

	return False

solve('06_sample.txt') # 41		6
solve('06_input.txt') # 4454	1503
