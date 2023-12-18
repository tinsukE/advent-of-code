# https://adventofcode.com/2023/day/9

def build_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	return [[int(value) for value in line.split()] for line in lines]

def diff_reduce(values):
	if all(value == 0 for value in values):
		return 0

	reduction = [values[i + 1] - values[i] for i in range(len(values) - 1)]
	return values[-1] + diff_reduce(reduction)

def diff_rreduce(values):
	if all(value == 0 for value in values):
		return 0

	reduction = [values[i + 1] - values[i] for i in range(len(values) - 1)]
	return values[0] - diff_rreduce(reduction)

def solve_1(filename):
	histories = build_input(filename)
	sum_reductions = sum([diff_reduce(history) for history in histories])
	print(filename, 'part 1:', sum_reductions)

def solve_2(filename):
	histories = build_input(filename)
	sum_reductions = sum([diff_rreduce(history) for history in histories])
	print(filename, 'part 2:', sum_reductions)


solve_1('09_sample.txt')
solve_1('09_input.txt')

solve_2('09_sample.txt')
solve_2('09_input.txt')