# https://adventofcode.com/2024/day/22

from collections import defaultdict

def parse_input(filename):
	file = open(filename, 'r')
	return [int(line.strip()) for line in file.readlines()]

def secret_random(number):
	number = (number ^ (number * 64)) % 16777216
	number = (number ^ int(number / 32)) % 16777216
	number = (number ^ (number * 2048)) % 16777216
	return number

def solve(filename):
	numbers = parse_input(filename)

	sum_numbers = 0
	sum_changes_bananas = defaultdict(int)
	max_bananas = None
	for number in numbers:
		last_4_changes = []
		changes_bananas = set()
		for _ in range(2000):
			next_number = secret_random(number)
			last_4_changes.append((next_number % 10) - (number % 10))
			number = next_number

			if len(last_4_changes) < 4:
				continue
			if len(last_4_changes) > 4:
				last_4_changes.pop(0)

			changes_tuple = tuple(last_4_changes)
			if changes_tuple not in changes_bananas:
				changes_bananas.add(changes_tuple)
				sum_changes_bananas[changes_tuple] += next_number % 10
				if max_bananas is None or sum_changes_bananas[changes_tuple] > max_bananas:
					max_bananas = sum_changes_bananas[changes_tuple]
		sum_numbers += number
	print('sum_numbers', sum_numbers)
	print('max_bananas', max_bananas)

solve('22_sample.txt') # 37327623, 24
solve('22_sample2.txt') # 37990510, 23
solve('22_input.txt') # 13584398738, 1612
