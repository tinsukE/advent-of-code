# https://adventofcode.com/2023/day/24

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	hailstones = []
	for line in [line.strip() for line in lines]:
		pos, vel = line.split(' @ ')
		pos = [int(value) for value in pos.split(', ')[0:-1]]
		vel = [int(value) for value in vel.split(', ')[0:-1]]
		hailstones.append((pos, vel))
	return hailstones

def intersection(hail1, hail2):
	(x1, y1) = hail1[0]
	(x2, y2) = (hail1[0][0] + hail1[1][0], hail1[0][1] + hail1[1][1])
	(x3, y3) = hail2[0]
	(x4, y4) = (hail2[0][0] + hail2[1][0], hail2[0][1] + hail2[1][1])

	denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
	if denominator == 0:
		return None

	x = ( (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4) ) / denominator
	y = ( (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4) ) / denominator
	return (x, y)

def is_within_bounds(cross, bounds):
	return cross and bounds[0] <= cross[0] and cross[0] <= bounds[1] and bounds[0] <= cross[1] and cross[1] <= bounds[1]

def is_ahead(hail, point):
	pos, vel = hail
	return (point[0] >= pos[0]) == (vel[0] >= 0) and (point[1] >= pos[1]) == (vel[1] >= 0)

def solve(filename, bounds):
	global DEBUG
	hailstones = parse_input(filename)
	if DEBUG:
		for hail in hailstones: print(hail)
	
	sum_cross = 0
	for i, hail1 in enumerate(hailstones):
		for hail2 in hailstones[i + 1:]:
			cross = intersection(hail1, hail2)
			if cross == None:
				continue
			if DEBUG: print(hail1, 'and', hail2, 'intersect at', cross)
			if is_within_bounds(cross, bounds) and is_ahead(hail1, cross) and is_ahead(hail2, cross):
				if DEBUG: print('inside and ahead!')
				sum_cross += 1
	print(filename, 'sum_cross', sum_cross)

DEBUG = False
solve('24_sample.txt', (7, 27))
solve('24_input.txt', (200000000000000, 400000000000000))
