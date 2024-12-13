# https://adventofcode.com/2024/day/12

from collections import defaultdict

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	return [line.strip() for line in lines]

def is_within_bounds(area_map, pos):
	return pos[0] >= 0 and pos[0] < len(area_map) and pos[1] >= 0 and pos[1] < len(area_map[0])

DELTAS = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
def deltas(pos):
	return [(d, (pos[0] + delta[0], pos[1] + delta[1])) for d, delta in DELTAS.items()]

regions = set()
def gen_region(plant):
	i = 0
	while True:
		region = plant + str(i)
		if region not in regions:
			regions.add(region)
			return region
		i += 1

def add_to_region(garden, plots, region, plot):
	if plot in plots:
		return
	plots[plot] = region
	for _, neighbor in deltas(plot):
		if is_within_bounds(garden, neighbor) and garden[neighbor[0]][neighbor[1]] == garden[plot[0]][plot[1]]:
			add_to_region(garden, plots, region, neighbor)

def calculate_plots(garden):
	plots = {}
	for i, row in enumerate(garden):
		for j, plant in enumerate(row):
			plot = (i, j)
			if plot in plots:
				continue
			region = gen_region(plant)
			add_to_region(garden, plots, region, plot)
	return plots

def perpendicular_neighbors(pos, neighbor):
	if pos[0] == neighbor[0]:
		return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]
	else:
		return [(pos[0], pos[1] - 1), (pos[0], pos[1] + 1)]

def solve(filename):
	garden = parse_input(filename)

	plots = calculate_plots(garden)

	areas = defaultdict(int)
	perimeters = defaultdict(int)

	# Part 1
	for i, row in enumerate(garden):
		for j, plant in enumerate(row):
			plot = (i, j)
			region = plots[plot]

			areas[region] += 1

			for _, neighbor in deltas(plot):
				if not is_within_bounds(garden, neighbor):
					perimeters[region] += 1
				elif garden[neighbor[0]][neighbor[1]] != plant:
					perimeters[region] += 1

	# Part 2
	sides = defaultdict(list)
	for i, row in enumerate(garden):
		for j, plant in enumerate(row):
			plot = (i, j)
			region = plots[plot]
			region_sides = sides[region]

			for d, neighbor in deltas(plot):
				if is_within_bounds(garden, neighbor) and garden[neighbor[0]][neighbor[1]] == plant:
					continue

				found_side = None
				for p_neigh in perpendicular_neighbors(plot, neighbor):
					if not is_within_bounds(garden, p_neigh):
						continue
					for region_side in region_sides:
						if (d, p_neigh) in region_side:
							found_side = region_side
							break
					if found_side is not None:
						break
				if found_side is None:
					found_side = set()
					region_sides.append(found_side)
				found_side.add((d, plot))

	cost = 0
	cost_bulk = 0
	for region, area in areas.items():
		# print(region, 'area:', area, 'perimeter:', perimeters[region], 'sides:', len(sides[region]))
		cost += area * perimeters[region]
		cost_bulk += area * len(sides[region])
	print('cost', cost)
	print('cost_bulk', cost_bulk)

solve('12_sample1.txt')	# 140 		80
solve('12_sample2.txt')	# 772 		436
solve('12_sample.txt')	# 1930 		206
solve('12_input.txt')	# 1467094 	881182
