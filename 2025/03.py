# https://adventofcode.com/2025/day/3

def parse_input(filename):
	file = open(filename, 'r')
	banks = []
	for line in [line.strip() for line in file.readlines()]:
		batteries = [int(c) for c in line]
		banks.append(batteries)
	return banks

def solve_1(filename):
	banks = parse_input(filename)

	sum_joltage = 0

	for bank in banks:
		decimal = max(bank[:-1])
		index = bank.index(decimal)
		unit = max(bank[index + 1:])
		# print("max for", bank, "=", decimal * 10 + unit)
		sum_joltage += decimal * 10 + unit

	print("sum_joltage", sum_joltage)

def solve_2(filename):
	banks = parse_input(filename)

	sum_joltage = 0

	for bank in banks:
		max_joltage = ""

		index = 0
		for length in range(11, -1, -1):
			sub_bank = bank[index:len(bank)-length]
			joltage = max(sub_bank)
			# print("found", joltage, "in", sub_bank)
			index += sub_bank.index(joltage) + 1
			max_joltage += str(joltage)

		# print("max for", bank, "=", max_joltage)
		sum_joltage += int(max_joltage)

	print("sum_joltage", sum_joltage)

solve_1('03_sample.txt') # 357
solve_1('03_input.txt') # 16842

solve_2('03_sample.txt') # 3121910778619
solve_2('03_input.txt') # 167523425665348
