# https://adventofcode.com/2023/day/5

file = open('05.in', 'r')
lines = file.readlines()

# part 1
inputs = {int(seed) for seed in lines[0].strip().split(':')[1].strip().split()}
print('inputs', inputs)
index = 1
while index + 2 < len(lines):
	index += 2

	output = set()
	while index < len(lines) and lines[index][0].isdigit():
		(dst_start, src_start, length) = [int(number) for number in lines[index].strip().split()]
		index += 1

		for input in list(inputs):
			if input >= src_start and input < src_start + length:
				inputs.remove(input)
				output.add(dst_start + input - src_start)

	output.update(inputs)
	inputs = output

print('min', min(output))
print()
print()



# part 2
from dataclasses import dataclass
@dataclass
class Interval:
	start: int
	length: int
	def last(self) -> int:
		return self.start + self.length - 1
	def offset(self, offset):
		return Interval(self.start + offset, self.length)
	def split_at(self, split):
		if split < self.start or split > self.last():
			raise ValueError('Can\'t split', self, 'at', split)
		return (Interval(self.start, split - self.start), Interval(split, self.last() - split + 1))
	def __lt__(self, other):
		return self.start < other.start

inputs = []
seeds = [int(seed) for seed in lines[0].strip().split(':')[1].strip().split()]
for index in range(0, len(seeds), 2):
	inputs.append(Interval(seeds[index], seeds[index + 1]))
print('inputs', inputs)

index = 1
while index + 2 < len(lines):
	index += 2

	output = []
	while index < len(lines) and lines[index][0].isdigit():
		(dst_start, src_start, length) = [int(number) for number in lines[index].strip().split()]
		src = Interval(src_start, length)
		offset = dst_start - src_start
		index += 1

		for interval in list(inputs):
			# interval is completely inside src
			if interval.start >= src.start and interval.last() <= src.last():
				inputs.remove(interval)
				output.append(interval.offset(offset))
			# interval starts inside src, and finishes later
			elif interval.start > src.start and interval.start <= src.last() and interval.last() > src.last():
				inputs.remove(interval)
				split = interval.split_at(src.last())
				output.append(split[0].offset(offset))
				inputs.append(split[1])
			# interval starts before src, and finishes inside
			elif interval.start < src.start and interval.last() >= src.start and interval.last() <= src.last():
				inputs.remove(interval)
				split = interval.split_at(src.start)
				inputs.append(split[0])
				output.append(split[1].offset(offset))
			# interval starts before src, and finishes later
			elif interval.start < src.start and interval.last() >= src.last():
				inputs.remove(interval)
				split = interval.split_at(src.start)
				inputs.append(split[0])
				split = split[1].split_at(src.last())
				output.append(split[0].offset(offset))
				inputs.append(split[1])

	output += inputs
	output = [interval for interval in output if interval.length > 0]
	inputs = output

print('min', min(output))
print('len', len(output))

