# https://adventofcode.com/2024/day/5

from functools import cmp_to_key

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	rules = []
	updates = []

	for line in lines:
		if "|" in line:
			rules.append(line.split("|"))
		elif "," in line:
			updates.append(line.split(","))

	return (rules, updates)

def is_correct_order(rules, update):
	pages = dict([(page, i) for (i, page) in enumerate(update)])

	for rule in rules:
		first = pages.get(rule[0])
		second = pages.get(rule[1])
		if first is None or second is None:
			continue
		if first > second:
			return False

	return True

def solve(filename):
	(rules, updates) = parse_input(filename)
	
	sum_correct_middles = 0
	sum_corrected_middles = 0

	for update in updates:
		if is_correct_order(rules, update):
			sum_correct_middles += int(update[int(len(update) / 2)])
			continue

		def compare_page(a, b):
			if [a, b] in rules:
				return -1
			if [b, a] in rules:
				return 1
			assert false, "Can't compare {} and {}".format(a, b)

		corrected = sorted(update, key=cmp_to_key(compare_page))
		sum_corrected_middles += int(corrected[int(len(corrected) / 2)])

	print("sum_correct_middles", sum_correct_middles)
	print("sum_corrected_middles", sum_corrected_middles)

solve('05_sample.txt') # 143	123
solve('05_input.txt') # 6267	5184
