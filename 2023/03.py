# https://adventofcode.com/2023/day/3

file = open('03.in', 'r')
matrix = [line.strip() for line in file.readlines()]
rows = len(matrix)
cols = len(matrix[0])
print(rows, cols)

def is_symbol(row, col):
	if row < 0 or col < 0 or row >= rows or col >= cols:
		return False
	char = matrix[row][col]
	return char != '.' and not char.isdigit()

def is_part(row, col, length):
	# top left, top right
	if is_symbol(row - 1, col - 1) or is_symbol(row - 1, col + length):
		return True
	# bottom left, bottom right
	if is_symbol(row + 1, col - 1) or is_symbol(row + 1, col + length):
		return True
	# left, right
	if is_symbol(row, col - 1) or is_symbol(row, col + length):
		return True
	# top, bottom
	for index in Interval(col, col + length):
		if is_symbol(row - 1, index) or is_symbol(row + 1, index):
			return True
	return False

part_numbers_sum = 0
for row, line in enumerate(matrix):
	number_start = -1
	for col, char in enumerate(line):
		if char.isdigit():
			if number_start == -1:
				number_start = col
		else:
			if number_start != -1:
				if is_part(row, number_start, col - number_start):
					part_numbers_sum += int(line[number_start:col])
				number_start = -1
	if number_start != -1 and is_part(row, number_start, cols):
		part_numbers_sum += int(line[number_start:cols])
print('part_numbers_sum', part_numbers_sum)

def is_number(row, col):
	if row < 0 or col < 0 or row >= rows or col >= cols:
		return False
	char = matrix[row][col]
	return char.isdigit()

def find_adjacent_number_coords(row, col):
	adjacent_number_coords = []
	# top left
	if is_number(row - 1, col - 1):
		adjacent_number_coords.append((row - 1, col - 1))
		if not is_number(row - 1, col) and is_number(row - 1, col + 1):
			adjacent_number_coords.append((row - 1, col + 1))
	# top
	elif is_number(row - 1, col):
		adjacent_number_coords.append((row - 1, col))
	# top right
	elif is_number(row - 1, col + 1):
		adjacent_number_coords.append((row - 1, col + 1))

	#left
	if is_number(row, col - 1):
		adjacent_number_coords.append((row, col - 1))
	#right
	if is_number(row, col + 1):
		adjacent_number_coords.append((row, col + 1))

	# bottom left
	if is_number(row + 1, col - 1):
		adjacent_number_coords.append((row + 1, col - 1))
		if not is_number(row + 1, col) and is_number(row + 1, col + 1):
			adjacent_number_coords.append((row + 1, col + 1))
	# bottom
	elif is_number(row + 1, col):
		adjacent_number_coords.append((row + 1, col))
	# bottom right
	elif is_number(row + 1, col + 1):
		adjacent_number_coords.append((row + 1, col + 1))

	return adjacent_number_coords

def resolve_part_number(coord):
	row = coord[0]
	col = coord[1]
	line = matrix[row]

	start = col
	for index in reversed(Interval(0, col)):
		if not line[index].isdigit():
			break
		start = index

	end = col
	for index in Interval(col, cols):
		if not line[index].isdigit():
			break
		end = index
	return int(line[start:end + 1])

def calculate_gear_ratio(row, col):
	adjacent_number_coords = find_adjacent_number_coords(row, col)
	if len(adjacent_number_coords) != 2:
		return 0

	print("adjacent_number_coords", adjacent_number_coords)
	part1 = resolve_part_number(adjacent_number_coords[0])
	part2 = resolve_part_number(adjacent_number_coords[1])
	print(part1, "part1", part2, "part2")

	return part1 * part2

gear_ratio_sum = 0
for row, line in enumerate(matrix):
	for col, char in enumerate(line):
		if char == '*':
			gear_ratio_sum += calculate_gear_ratio(row, col)
print('gear_ratio_sum', gear_ratio_sum)