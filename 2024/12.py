# https://adventofcode.com/2024/day/12

from collections import defaultdict

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	return [line.strip() for line in lines]

def is_within_bounds(area_map, pos):
	return pos[0] >= 0 and pos[0] < len(area_map) and pos[1] >= 0 and pos[1] < len(area_map[0])

DELTAS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
def deltas(pos):
	return [(pos[0] + delta[0], pos[1] + delta[1]) for delta in DELTAS]

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
	for neighbor in deltas(plot):
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

def solve(filename):
	garden = parse_input(filename)
	# print(garden)

	plots = calculate_plots(garden)

	areas = defaultdict(int)
	perimeters = defaultdict(int)

	for i, row in enumerate(garden):
		for j, plant in enumerate(row):
			plot = (i, j)
			region = plots[plot]

			areas[region] += 1

			for neighbor in deltas(plot):
				if not is_within_bounds(garden, neighbor):
					perimeters[region] += 1
				elif garden[neighbor[0]][neighbor[1]] != plant:
					perimeters[region] += 1

	# print('areas', areas)
	# print('perimeters', perimeters)
	# print('plots', plots)

	cost = 0
	for region, area in areas.items():
		# print(region, 'area:', area, 'perimeter:', perimeters[region])
		cost += area * perimeters[region]
	print('cost', cost)

solve('12_sample1.txt')	# 140
solve('12_sample2.txt')	# 772
solve('12_sample.txt')	# 1930
solve('12_input.txt')	# 1467094
