# https://adventofcode.com/2025/day/6

def parse_input(filename):
	file = open(filename, 'r')
	numbers = []
	ops = []
	for line in [line.strip() for line in file.readlines()]:
		if line[0] == '*' or line[0] == '+':
			ops = line.split()
		else:
			numbers.append([int(number) for number in line.split()])
	return numbers, ops

def solve_1(filename):
	numbers, ops = parse_input(filename)

	grand_total = 0
	for i in range(len(ops)):
		op = ops[i]
		total = 1 if op == '*' else 0

		for n in range(len(numbers)):
			if op == '*':
				total *= numbers[n][i]
			else:
				total += numbers[n][i]
		grand_total += total

	print("grand_total", grand_total)

def read_number(sheet, j):
	number = ""
	for i in range(len(sheet)):
		if sheet[i][j] != ' ':
			number += sheet[i][j]
	return int(number)

def solve_2(filename):
	file = open(filename, 'r')
	lines = [line.rstrip('\n\r') for line in file.readlines()]
	sheet = lines[0:-1]
	ops = lines[-1]

	grand_total = 0
	j = len(ops) - 1
	while j > 0:
		end = j
		while ops[j] == ' ':
			j -= 1
		start = j
		op = ops[j]
		j -= 2

		numbers = [read_number(sheet, nj) for nj in range(start, end + 1)]

		total = 1 if op == '*' else 0
		for number in numbers:
			if op == '*':
				total *= number
			else:
				total += number
		grand_total += total

	print("grand_total", grand_total)

solve_1('06_sample.txt') # 4277556
solve_1('06_input.txt') # 6371789547734

solve_2('06_sample.txt') # 3263827
solve_2('06_input.txt') # 11419862653216
