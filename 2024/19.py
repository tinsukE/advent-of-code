# https://adventofcode.com/2024/day/19

from functools import cache

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	return lines[0].strip().split(', '), [l.strip() for l in lines[2:]]

def is_possible(towels, pattern):
	for towel in towels:
		if towel == pattern:
			return True
		if pattern.startswith(towel) and is_possible(towels, pattern[len(towel):]):
			return True
	return False

@cache
def count_possible(towels, pattern):
	count = 0
	for towel in towels:
		if towel == pattern:
			count += 1
		elif pattern.startswith(towel):
			count += count_possible(towels, pattern[len(towel):])
	return count

def solve(filename):
	towels, patterns = parse_input(filename)
	possible = sum([is_possible(towels, pattern) for pattern in patterns])
	print('possible', possible)
	possible = sum([count_possible(tuple(towels), pattern) for pattern in patterns])
	print('count_possible', possible)

solve('19_sample.txt') # 6, 16
solve('19_input.txt') # 213, 1016700771200474
