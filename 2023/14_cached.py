# https://adventofcode.com/2023/day/13

from functools import cache

def calculate_load(platform):
	load_sum = 0
	for i, row in enumerate(platform):
		for item in row:
			if item == 'O':
				load_sum += len(platform) - i
	return load_sum

def roll_north(platform):
	for i, row in enumerate(platform):
		if i == 0:
			continue
		for j, item in enumerate(row):
			if item != 'O':
				continue
			dest_i = i
			for test_i in range(i, -1, -1):
				if test_i == 0:
					dest_i = test_i
					break
				if platform[test_i - 1][j] != '.':
					dest_i = test_i
					break
			if dest_i != i:
				platform[dest_i][j] = 'O'
				platform[i][j] = '.'

def roll_south(platform):
	for i, row in reversed(list(enumerate(platform))):
		if i == len(platform) - 1: continue
		for j, item in enumerate(row):
			if item != 'O':
				continue
			dest_i = i
			for test_i in range(i, len(platform)):
				if test_i == len(platform) - 1:
					dest_i = test_i
					break
				if platform[test_i + 1][j] != '.':
					dest_i = test_i
					break
			if dest_i != i:
				platform[dest_i][j] = 'O'
				platform[i][j] = '.'

def roll_west(platform):
	for i, row in enumerate(platform):
		for j, item in enumerate(row):
			if j == 0 or item != 'O':
				continue
			dest_j = j
			for test_j in range(j, -1, -1):
				if test_j == 0:
					dest_j = test_j
					break
				if platform[i][test_j - 1] != '.':
					dest_j = test_j
					break
			if dest_j != j:
				platform[i][dest_j] = 'O'
				platform[i][j] = '.'

def roll_east(platform):
	for i, row in enumerate(platform):
		for j, item in reversed(list(enumerate(row))):
			if j == len(row) - 1 or item != 'O':
				continue
			dest_j = j
			for test_j in range(j, len(row)):
				if test_j == len(row) - 1:
					dest_j = test_j
					break
				if platform[i][test_j + 1] != '.':
					dest_j = test_j
					break
			if dest_j != j:
				platform[i][dest_j] = 'O'
				platform[i][j] = '.'

@cache
def run_cycle(platform):
	new_platform = [list(row) for row in platform]
	roll_north(new_platform)
	roll_west(new_platform)
	roll_south(new_platform)
	roll_east(new_platform)
	return tuple([tuple(row) for row in new_platform])

def solve_1(filename):
	file = open(filename, 'r')
	platform = [[char for char in line.strip()] for line in file.readlines()]

	roll_north(platform)
	print(filename, 'part 1 load_sum', calculate_load(platform))

def solve_2(filename, cycles):
	file = open(filename, 'r')
	platform = tuple([tuple([char for char in line.strip()]) for line in file.readlines()])

	result_index = {}
	loop = None
	for i in range(cycles):
		result_index[platform] = i
		platform = run_cycle(platform)
		loop_index = result_index.get(platform)
		if loop_index:
			loop = (loop_index, i)
			break
	if not loop:
		print(filename, cycles, 'part 2 load_sum', calculate_load(platform))
	else:
		rest_cycles = (cycles - loop[0]) % (loop[1] - loop[0] + 1)
		for _ in range(rest_cycles):
			platform = run_cycle(platform)
		print(filename, cycles, 'part 2 load_sum', calculate_load(platform))

solve_1('14_sample.txt')
solve_1('14_input.txt')

solve_2('14_sample.txt', 3)
solve_2('14_sample.txt', 30)
solve_2('14_sample.txt', 1000)
solve_2('14_sample.txt', 1000000000)
solve_2('14_input.txt', 1000000000)
