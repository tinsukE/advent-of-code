# https://adventofcode.com/2023/day/8

from math import lcm

def build_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()

	instructions = lines[0].strip()

	directions = {}
	for line in [line.strip() for line in lines[2:]]:
		(source, dest) = line.split(' = ')
		(dest_left, dest_right) = dest.strip('()').split(', ')
		directions[source] = (dest_left, dest_right)
	return (instructions, directions)

def navigate(instructions, directions, start, end_condition):
	current = start
	instruction_index = 0
	steps = 0
	while not end_condition(current):
		direction_index = 0 if instructions[instruction_index] == 'L' else 1
		current = directions[current][direction_index]

		instruction_index = (instruction_index + 1) % len(instructions)
		steps += 1
	return steps

def solve_1(filename):
	(instructions, directions) = build_input(filename)

	steps = navigate(instructions, directions, 'AAA', lambda position: position == 'ZZZ')

	print(filename, 'part 1 steps:', steps)

def solve_2(filename):
	(instructions, directions) = build_input(filename)

	starts = [key for key in directions.keys() if key[-1] == 'A']
	steps = [navigate(instructions, directions, start, lambda position: position[-1] == 'Z') for start in starts]
	
	print(filename, 'part 2 steps:', lcm(*steps))

solve_1('08_sample.txt')
solve_1('08_input.txt')

solve_2('08_sample2.txt')
solve_2('08_input.txt')
