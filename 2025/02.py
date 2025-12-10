# https://adventofcode.com/2025/day/2

import math
from functools import cache

def parse_input(filename):
	file = open(filename, 'r')
	ranges = []
	for line in [line.strip() for line in file.readlines()]:
		id_ranges = line.split(',')
		for id_range in id_ranges:
			a, b = id_range.split('-')
			ranges.append([a, b])
	return ranges

def is_invalid_id_str(id):
	id_str = str(id)
	if len(id_str) % 2 == 0:
		half_len = len(id_str) // 2
		if id_str[:half_len] == id_str[half_len:]:
			return True
	return False

def is_invalid_id_math(id):
	digits = int(math.log10(id)) + 1
	if digits % 2 == 1:
		return False

	half_digits = digits // 2
	decimals = 10 ** half_digits

	left = id  // decimals
	right = id % decimals

	return left == right

def solve_1(filename):
	ranges = parse_input(filename)

	sum_invalid_ids = 0
	for (start, end) in ranges:
		for id in range(int(start), int(end) + 1):
			if is_invalid_id_str(id):
				sum_invalid_ids += id

			# How is this slower?!?!
			# if is_invalid_id_math(id):
			# 	sum_invalid_ids += id

	print("sum_invalid_ids", sum_invalid_ids)

# Yup, also slower
# @cache
def matches_pattern(pattern, string):
	if len(pattern) > len(string):
		return False
	elif len(pattern) == len(string):
		return pattern == string
	else:
		return pattern == string[:len(pattern)] and matches_pattern(pattern, string[len(pattern):])

def is_invalid_id_2(id):
	id_str = str(id)
	for i in range(len(id_str) // 2):
		pattern = id_str[:i + 1]
		if matches_pattern(pattern, id_str[i + 1:]):
			return True
	return False

def solve_2(filename):
	ranges = parse_input(filename)

	sum_invalid_ids = 0
	for (start, end) in ranges:
		for id in range(int(start), int(end) + 1):
			if is_invalid_id_2(id):
				sum_invalid_ids += id

	print("sum_invalid_ids", sum_invalid_ids)

solve_1('02_sample.txt') # 1227775554
solve_1('02_input.txt') # 28844599675

solve_2('02_sample.txt') # 4174379265
solve_2('02_input.txt') # 48778605167
