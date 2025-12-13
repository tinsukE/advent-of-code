# https://adventofcode.com/2025/day/7

# pip install ordered_set
from ordered_set import OrderedSet
from collections import OrderedDict

def parse_input(filename):
	file = open(filename, 'r')
	grid = [line.strip() for line in file.readlines()]
	start = None
	for i, line in enumerate(grid):
		for j, item in enumerate(line):
			if item == 'S':
				start = (i, j)
				break;
		if start:
			break
	return grid, start

def solve_1(filename):
	grid, start = parse_input(filename)

	beams = OrderedSet()
	beams.append((start[0] + 1, start[1]))
	count_splits = 0

	while len(beams) > 0:
		beam = beams.pop(0)
		if beam[0] + 1 >= len(grid):
			continue
		elif grid[beam[0] + 1][beam[1]] == '^':
			count_splits += 1
			if beam[1] > 0:
				beams.append((beam[0] + 1, beam[1] - 1))
			if beam[1] + 1 < len(grid[0]):
				beams.append((beam[0] + 1, beam[1] + 1))
		else:
			beams.append((beam[0] + 1, beam[1]))

	print("count_splits", count_splits)

def solve_2(filename):
	grid, start = parse_input(filename)

	beams_weight = OrderedDict()
	beams_weight[(start[0] + 1, start[1])] = 1
	count_timelines = 0

	while len(beams_weight) > 0:
		(beam, weight) = beams_weight.popitem(last = False)
		if beam[0] + 1 >= len(grid):
			count_timelines += weight
			continue
		elif grid[beam[0] + 1][beam[1]] == '^':
			if beam[1] > 0:
				new_beam = (beam[0] + 1, beam[1] - 1)
				new_weight = weight + beams_weight.get(new_beam, 0)
				beams_weight[new_beam] = new_weight
			if beam[1] + 1 < len(grid[0]):
				new_beam = (beam[0] + 1, beam[1] + 1)
				new_weight = weight + beams_weight.get(new_beam, 0)
				beams_weight[new_beam] = new_weight
		else:
			new_beam = (beam[0] + 1, beam[1])
			new_weight = weight + beams_weight.get(new_beam, 0)
			beams_weight[new_beam] = new_weight

	print("count_timelines", count_timelines)

solve_1('07_sample.txt') # 21
solve_1('07_input.txt') # 1717

solve_2('07_sample.txt') # 40
solve_2('07_input.txt') # 231507396180012
