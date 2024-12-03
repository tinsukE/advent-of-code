# https://adventofcode.com/2024/day/3

import re

def parse_input(filename):
	file = open(filename, 'r')
	return file.read()

def perform_muls(row):
	muls = re.findall("mul\\(\\d{1,3},\\d{1,3}\\)", row)
	sum_muls = 0
	for mul in muls:
		numbers = re.findall("\\d{1,3}", mul)
		sum_muls += int(numbers[0]) * int(numbers[1])
	return sum_muls

def solve(filename):
	memory = parse_input(filename)
	
	sum_muls = perform_muls(memory)

	print("sum_muls", sum_muls)

def solve_2(filename):
	memory = parse_input(filename)
	
	sum_muls = 0
	index = 0
	while index < len(memory):
		match = re.search("don't\\(\\)", memory[index:])
		end = index + match.start() if match is not None else len(memory)

		sum_muls += perform_muls(memory[index:end])

		match = re.search("do\\(\\)", memory[end:])
		index = end + match.start() if match is not None else len(memory)

	print("sum_muls", sum_muls)


solve('03_sample.txt') # 161
solve('03_input.txt') # 185797128

solve_2('03_sample2.txt') # 48
solve_2('03_input.txt') # 89798695
