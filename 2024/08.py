# https://adventofcode.com/2024/day/7

from collections import defaultdict

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	frequency_map = defaultdict(list)
	for i, line in enumerate(lines):
		for j, char in enumerate(line):
			if char == ".":
				continue
			frequency_map[char].append((i, j))

	return frequency_map, len(lines), len(lines[0])

def is_within_bounds(rows, cols, pos):
	return pos[0] >= 0 and pos[0] < rows and pos[1] >= 0 and pos[1] < cols

def antinode(pos_a, pos_b, delta, multiplier):
	return (pos_a[0] + (delta[0] if pos_a[0] > pos_b[0] else -delta[0]) * multiplier, \
		pos_a[1] + (delta[1] if pos_a[1] > pos_b[1] else -delta[1]) * multiplier)

def solve(filename):
	frequency_map, rows, cols = parse_input(filename)

	antinodes = set()
	harmonic_antinodes = set()

	for (frequency, positions) in frequency_map.items():
		if len(positions) > 1:
			harmonic_antinodes.update(positions)

		for i, pos_a in enumerate(positions[:-1]):
			for pos_b in positions[i + 1:]:
				delta = (abs(pos_a[0] - pos_b[0]), abs(pos_a[1] - pos_b[1]))

				# Part 1
				ant_a = antinode(pos_a, pos_b, delta, 1)
				if is_within_bounds(rows, cols, ant_a):
					antinodes.add(ant_a)
				ant_b = antinode(pos_b, pos_a, delta, 1)
				if is_within_bounds(rows, cols, ant_b):
					antinodes.add(ant_b)

				# Part 2
				multiplier = 1
				while is_within_bounds(rows, cols, ant_a):
					harmonic_antinodes.add(ant_a)
					multiplier += 1
					ant_a = antinode(pos_a, pos_b, delta, multiplier)
				multiplier = 1
				while is_within_bounds(rows, cols, ant_b):
					harmonic_antinodes.add(ant_b)
					multiplier += 1
					ant_b = antinode(pos_b, pos_a, delta, multiplier)


	print("len(antinodes)", len(antinodes))
	print("len(harmonic_antinodes)", len(harmonic_antinodes))

solve('08_sample.txt') # 14	34
solve('08_input.txt') # 364	1231
