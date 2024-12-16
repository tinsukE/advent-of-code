# https://adventofcode.com/2024/day/11

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	start = None
	end = None
	for i, line in enumerate(lines):
		if 'S' in line:
			start = (i, line.index('S'))
		if 'E' in line:
			end = (i, line.index('E'))
	return [line.strip() for line in lines], start, end

def print_area(area):
	for line in area:
		for char in line:
			print(char, end='')
		print()

def solve(filename):
	area, start, end = parse_input(filename)
	print_area(area)
	print(start, end)

solve('16_sample1.txt')
