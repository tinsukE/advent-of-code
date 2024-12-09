# https://adventofcode.com/2024/day/7

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	equations = []
	for line in lines:
		value, numbers = line.split(":")
		value = int(value)
		numbers = [int(number) for number in numbers.strip().split(" ")]
		equations.append((value, numbers))

	return equations

def op_sum(a, b):
	return a + b

def op_mult(a, b):
	return a * b

def op_concat(a, b):
	multiplier = 1
	mult_b = b
	while mult_b > 1:
		mult_b = int(mult_b / 10)
		multiplier *= 10
	return a * multiplier + b

def is_possible(ops, value, numbers, current = None):
	if current is None:
		return is_possible(ops, value, numbers[1:], numbers[0])

	if current > value:
		return False

	if len(numbers) == 0:
		return value == current

	return any(is_possible(ops, value, numbers[1:], op(current, numbers[0])) for op in ops)

def solve(filename):
	equations = parse_input(filename)

	ops = [op_sum, op_mult]
	result = sum(value for (value, numbers) in equations if is_possible(ops, value, numbers))
	print("result_1", result)

	ops = [op_sum, op_mult, op_concat]
	result = sum(value for (value, numbers) in equations if is_possible(ops, value, numbers))
	print("result_2", result)

solve('07_sample.txt') # 3749, 11387
solve('07_input.txt') # 303766880536, 64954130205514
