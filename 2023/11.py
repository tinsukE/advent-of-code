# https://adventofcode.com/2023/day/11

def expanded_universe(universe):
	rows = set()
	for row in range(len(universe)):
		if not [point for point in [universe[row][col] for col in range(len(universe[0]))] if point == '#']:
			rows.add(row)
	cols = set()
	for col in range(len(universe[0])):
		if not [point for point in [universe[row][col] for row in range(len(universe))] if point == '#']:
			cols.add(col)
	return (rows, cols)

def find_galaxies(universe):
	galaxies = []
	for row in range(len(universe)):
		for col in range(len(universe[0])):
			if universe[row][col] == '#':
				galaxies.append((row, col))
	return galaxies

def solve(filename, multiplier = 2):
	file = open(filename, 'r')
	universe = [line.strip() for line in file.readlines()]

	(exp_rows, exp_cols) = expanded_universe(universe)
	galaxies = find_galaxies(universe)

	sum_distance = 0
	for index, galaxy in enumerate(galaxies):
		for other in galaxies[index + 1:]:
			distance = abs(galaxy[0] - other[0]) + abs(galaxy[1] - other[1])
			rows = [row for row in range(min(galaxy[0], other[0]) + 1, max(galaxy[0], other[0]))]
			distance += len([row for row in rows if row in exp_rows]) * (multiplier - 1)
			cols = [col for col in range(min(galaxy[1], other[1]) + 1, max(galaxy[1], other[1]))]
			distance += len([col for col in cols if col in exp_cols]) * (multiplier - 1)
			sum_distance += distance
	print(filename, multiplier, 'sum distances:', sum_distance)

solve('11_sample.txt')
solve('11_input.txt')

solve('11_sample.txt', 10)
solve('11_sample.txt', 100)
solve('11_input.txt', 1000000)
