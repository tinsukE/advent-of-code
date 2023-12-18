# https://adventofcode.com/2023/day/13

def calculate_load(platform):
	load_sum = 0
	for i, row in enumerate(platform):
		for item in row:
			if item == 'O':
				load_sum += len(platform) - i
	return load_sum

def roll_north(platform):
	for j in range(len(platform[0])):
		rocks_count = 0
		for i in range(len(platform) - 1, -2, -1):
			item = platform[i][j] if i >= 0 else None
			if item == 'O':
				platform[i][j] = '.'
				rocks_count += 1
			if i == -1 or item == '#':
				for x in range(rocks_count):
					platform[i + x + 1][j] = 'O'
				rocks_count = 0

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

# def roll_north(platform):
# 	for j in range(len(platform[0])):
# 		rocks_count = 0
# 		for i in range(len(platform) - 1, -2, -1):
# 			item = platform[i][j] if i >= 0 else None
# 			if item == 'O':
# 				platform[i][j] = '.'
# 				rocks_count += 1
# 			if i == -1 or item == '#':
# 				for x in range(rocks_count):
# 					platform[i + x + 1][j] = 'O'
# 				rocks_count = 0

def roll_west2(platform):
	cols = len(platform[0])
	for i in range(len(platform)):
		rocks_count = 0
		for j in range(cols - 1, -2, -1):
			item = platform[i][j] if j >= 0 else None
			if item == 'O':
				platform[i][j] = '.'
				rocks_count += 1
			if j == -1 or item == '#':
				for y in range(rocks_count):
					platform[i][j + y + 1] = 'O'
				rocks_count = 0

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

def solve_1(filename):
	file = open(filename, 'r')
	platform = [[char for char in line.strip()] for line in file.readlines()]

	roll_north(platform)
	print(filename, 'part 1 load_sum', calculate_load(platform))

def solve_2(filename, cycles):
	file = open(filename, 'r')
	platform = [[char for char in line.strip()] for line in file.readlines()]

	for i in range(cycles):
		roll_north(platform)
		roll_west2(platform)
		roll_south(platform)
		roll_east(platform)

	print(filename, cycles, 'part 2 load_sum', calculate_load(platform))

solve_1('14_sample.txt')
solve_1('14_input.txt')

solve_2('14_sample.txt', 3)
solve_2('14_sample.txt', 30)
solve_2('14_sample.txt', 1000)
# solve_2('14_sample.txt', 1000000000)
