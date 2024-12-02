# https://adventofcode.com/2024/day/2

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]
	reports = []
	for line in lines:
		reports.append([int(level) for level in line.split(' ')])
	return reports

def report_without_level_at(report, index):
	return [level for i, level in enumerate(report) if i != index]

def is_safe_report(report, tolerant = False):
	direction = report[1] - report[0]
	safe = True
	for i, level in enumerate(report[:-1]):
		next_level = report[i + 1]
		diff = next_level - level
		if (diff > 0) != (direction > 0) or abs(diff) < 1 or abs(diff) > 3:
			if tolerant:
				# Try removing the two offending levels, i and in + 1
				# But also the two first ones, as they define the direction
				return is_safe_report(report_without_level_at(report, i)) or \
					is_safe_report(report_without_level_at(report, i + 1)) or \
					is_safe_report(report_without_level_at(report, 0)) or \
					is_safe_report(report_without_level_at(report, 1))
			else:
				safe = False
				break
	return safe


def solve(filename, tolerant = False):
	reports = parse_input(filename)
	safe_count = 0

	for report in reports:
		if is_safe_report(report, tolerant = tolerant):
			safe_count += 1

	print("safe_count", safe_count)


solve('02_sample.txt') # 2
solve('02_input.txt') # 236

solve('02_sample.txt', tolerant = True) # 4
solve('02_input.txt', tolerant = True) # 308
