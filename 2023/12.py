# https://adventofcode.com/2023/day/12

from functools import cache

@cache
def count_possibilities(springs, damaged):
	if len(springs) == 0:
		return 1 if len(damaged) == 0 else 0

	if len(springs) == 1:
		if len(damaged) > 1:
			return 0
		elif len(damaged) == 1 and damaged[0] == 1 and (springs[0] == '#' or springs[0] == '?'):
			return 1
		elif len(damaged) == 0 and (springs[0] == '.' or springs[0] == '?'):
			return 1
		else:
			return 0

	if springs[0] == '.':
		return count_possibilities(springs[1:], damaged)
	elif springs[0] == '#':
		if len(damaged) == 0:
			return 0
		elif damaged[0] == 1:
			if springs[1] == '#':
				return 0
			else:
				return count_possibilities(springs[2:], damaged[1:])
		else: # damaged[0] > 1:
			if springs[1] == '.':
				return 0
			elif springs[1] == '?':
				new_springs = list(springs[1:])
				new_springs[0] = '#'
			else:
				new_springs = springs[1:]

			new_damaged = list(damaged)
			new_damaged[0] = new_damaged[0] - 1
			return count_possibilities(tuple(new_springs), tuple(new_damaged))
	else: # springs[0] == '?':
		new_springs = list(springs)
		new_springs[0] = '.'
		a = count_possibilities(tuple(new_springs), damaged)
		new_springs[0] = '#'
		b = count_possibilities(tuple(new_springs), damaged)
		return a + b

def unfold(collection, folds, separator = None):
	unfolded_collection = []
	for i in range(folds):
		if separator and i > 0:
			unfolded_collection.append(separator)
		unfolded_collection += collection
	return unfolded_collection

def solve(filename, folds = 1):
	file = open(filename, 'r')

	sum_possibilities = 0
	for line in file.readlines():
		springs, damaged = line.strip().split()
		springs = unfold([char for char in springs], folds, '?')
		damaged = unfold([int(number) for number in damaged.split(',')], folds)

		possibilities = count_possibilities(tuple(springs), tuple(damaged))
		sum_possibilities += possibilities
	print(filename, 'folds:', folds, 'possibilities:', sum_possibilities)

solve('12_sample.txt')
solve('12_input.txt')

solve('12_sample.txt', 5)
solve('12_input.txt', 5)
