# https://adventofcode.com/2023/day/15

from collections import OrderedDict

def HASH(str):
	hash_value = 0
	for char in str:
		ascii_value = ord(char)
		hash_value += ascii_value
		hash_value *= 17
		hash_value = hash_value % 256
	return hash_value

def solve_1(filename):
	file = open(filename, 'r')
	line = file.readlines()[0].strip()
	steps = line.split(',')

	sum_hash = 0
	current_hash = 0
	for step in steps:
		sum_hash += HASH(step)

	print(filename, 'sum_hash', sum_hash)

def solve_2(filename):
	file = open(filename, 'r')
	line = file.readlines()[0].strip()
	steps = line.split(',')

	boxes = [OrderedDict() for _ in range(256)]

	for step in steps:
		if step[-1] == '-':
			label = step[0:-1]
			box = boxes[HASH(label)]
			box.pop(label, None)
		else:
			label, focal_length = step.split('=')
			box = boxes[HASH(label)]
			box[label] = int(focal_length)

	focusing_power = 0
	for i, box in enumerate(boxes):
		for j, lens in enumerate(box):
			focusing_power += (i + 1) * (j + 1) * box[lens]
	print(filename, 'focusing_power', focusing_power)

solve_1("15_sample.txt")
solve_1("15_input.txt")

solve_2("15_sample.txt")
solve_2("15_input.txt")
