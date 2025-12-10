# https://adventofcode.com/2025/day/5

def parse_input(filename):
	file = open(filename, 'r')
	fresh_ranges = []
	ids = []
	reading_ranges = True
	for line in [line.strip() for line in file.readlines()]:
		if len(line) == 0:
			reading_ranges = False
		elif reading_ranges:
			start, end = line.split('-')
			fresh_ranges.append((int(start), int(end)))
		else:
			ids.append(int(line))
	return fresh_ranges, ids

def id_in_range(id, fresh_range):
	return id >= fresh_range[0] and id <= fresh_range[1]

def solve_1(filename):
	fresh_ranges, ids = parse_input(filename)

	sum_fresh_ids = 0
	for id in ids:
		if any(id_in_range(id, fresh_range) for fresh_range in fresh_ranges):
			sum_fresh_ids += 1

	print("sum_fresh_ids", sum_fresh_ids)

def id_ranges_overlap(id_range_a, id_range_b):
	return id_in_range(id_range_a[0], id_range_b) or id_in_range(id_range_a[1], id_range_b) \
		or id_in_range(id_range_b[0], id_range_a) or id_in_range(id_range_b[1], id_range_a)

def merge_id_ranges(id_range_a, id_range_b):
	return (min(id_range_a[0], id_range_b[0]), max(id_range_a[1], id_range_b[1]))

def solve_2(filename):
	id_ranges, _ = parse_input(filename)
	merged_id_ranges = []

	while len(id_ranges) > 0:
		id_range = id_ranges.pop(0)

		for merged_id_range in merged_id_ranges[:]:
			if id_ranges_overlap(id_range, merged_id_range):
				merged_id_ranges.remove(merged_id_range)
				id_range = merge_id_ranges(id_range, merged_id_range)

		merged_id_ranges.append(id_range)

	# print("merged_id_ranges", merged_id_ranges)
	max_fresh_ids = 0
	for id_range in merged_id_ranges:
		max_fresh_ids += id_range[1] - id_range[0] + 1

	print("max_fresh_ids", max_fresh_ids)

solve_1('05_sample.txt') # 3
solve_1('05_input.txt') # 690

solve_2('05_sample.txt') # 14
solve_2('05_input.txt') # 344323629240733
