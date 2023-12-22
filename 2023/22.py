# https://adventofcode.com/2023/day/17

from functools import reduce

def parse_input(filename):
	file = open(filename, 'r')
	bricks = []
	for line in file.readlines():
		start, end = line.split('~')
		brick = (tuple([int(coord) for coord in start.split(',')]), tuple([int(coord) for coord in end.split(',')]))
		if brick[0][0] > brick[1][0] or brick[0][1] > brick[1][1] or brick[0][2] > brick[1][2]:
			raise ValueError("This wasn't supposed to happen...")
		bricks.append(brick)
	return sorted(bricks, key=lambda brick:brick[0][2])

def intersect_in(a0, a1, b0, b1):
	return a0 <= b1 and b0 <= a1

def intersect_in_xy(brick_a, brick_b):
	return intersect_in(brick_a[0][0], brick_a[1][0], brick_b[0][0], brick_b[1][0]) and \
		intersect_in(brick_a[0][1], brick_a[1][1], brick_b[0][1], brick_b[1][1])
	pass

def brick_height(brick):
	return brick[1][2] - brick[0][2] + 1

def solve_1(filename):
	bricks = parse_input(filename)

	bricks_per_height = {}
	free_bricks = set(bricks)

	for brick in bricks:
		placed = False
		for z in range(brick[0][2] - 1, 0, -1):
			bricks_in_z = bricks_per_height.get(z)
			if bricks_in_z == None:
				continue

			intersected = set()
			for brick_in_z in bricks_in_z:
				if intersect_in_xy(brick, brick_in_z):
					# brick rests on top of brick_in_z
					bricks_per_height.setdefault(z + brick_height(brick), set()).add(brick)
					intersected.add(brick_in_z)
					placed = True
			if len(intersected) == 1:
				free_bricks.discard(intersected.pop())
			if placed:
				break
		if not placed:
			bricks_per_height.setdefault(brick_height(brick), set()).add(brick)

	print(filename, 'free_bricks', len(free_bricks))

def solve_2(filename):
	bricks = parse_input(filename)

	bricks_per_height = {}
	brick_supports_map = {}
	bricks_supported_by_map = {}

	for brick in bricks:
		placed = False
		for z in range(brick[0][2] - 1, 0, -1):
			bricks_in_z = bricks_per_height.get(z)
			if bricks_in_z == None:
				continue

			for brick_in_z in bricks_in_z:
				if intersect_in_xy(brick, brick_in_z):
					# brick rests on top of brick_in_z
					bricks_per_height.setdefault(z + brick_height(brick), set()).add(brick)
					brick_supports_map.setdefault(brick_in_z, set()).add(brick)
					bricks_supported_by_map.setdefault(brick, set()).add(brick_in_z)
					placed = True
			if placed:
				break
		if not placed:
			bricks_per_height.setdefault(brick_height(brick), set()).add(brick)

	def dropped_bricks(fallen_bricks):
		if len(fallen_bricks) == 0:
			return 0

		min_height = min([brick_height(b) - fallen_bricks[b] for b in fallen_bricks])
		current_fallen_bricks = set([b for b in fallen_bricks if brick_height(b) - fallen_bricks[b] == min_height])

		supported_bricks = set()
		for bricks in [brick_supports_map.get(fallen_brick) for fallen_brick in current_fallen_bricks]:
			supported_bricks.update(bricks if bricks != None else set())

		surviving_bricks = {key: value + min_height for key, value in fallen_bricks.items() if key not in current_fallen_bricks}

		new_fallen_bricks = set()
		for supported_brick in supported_bricks:
			if all([brick in current_fallen_bricks for brick in bricks_supported_by_map[supported_brick]]):
				new_fallen_bricks.add(supported_brick)
				surviving_bricks[supported_brick] = 0

		return len(new_fallen_bricks) + dropped_bricks(surviving_bricks)

	sum_falling = sum([dropped_bricks({b: 0}) for b in bricks])
	print(filename, 'sum_falling', sum_falling)

solve_1('22_sample.txt') # 5
solve_1('22_input.txt') # 480

solve_2('22_sample.txt') # 7
solve_2('22_input.txt') # 70348 < ?
