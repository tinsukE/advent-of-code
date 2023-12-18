# https://adventofcode.com/2023/day/5

import time

start = time.time()

file = open('05.in', 'r')
lines = file.readlines()

# part 1
ranges = [int(seed) for seed in lines[0].strip().split(':')[1].strip().split()]
inputs = []
for index in range(0, len(ranges), 2):
	inputs += [seed for seed in range(ranges[index], ranges[index] + ranges[index + 1])]
print('input len', len(inputs))

create_set = time.time()
inputs = set(inputs)
print('create set:', time.time() - create_set)

print('building input:', time.time() - start)

index = 1
while index + 2 < len(lines):
	block_start = time.time()
	index += 2

	output = set()
	while index < len(lines) and lines[index][0].isdigit():
		line_start = time.time()

		(dst_start, src_start, length) = [int(number) for number in lines[index].strip().split()]
		index += 1

		for input in list(inputs):
			if input >= src_start and input < src_start + length:
				inputs.remove(input)
				output.add(dst_start + input - src_start)

		print('one line:', time.time() - line_start)

	output.update(inputs)
	inputs = output
	print('one block:', time.time() - block_start)

mapping = time.time()
print('mapping:', mapping - start)

print('min', min(output))

print('result:', time.time() - start)