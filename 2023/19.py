# https://adventofcode.com/2023/day/19

from dataclasses import dataclass
from functools import reduce

@dataclass
class Rule:
	check: str
	dest: str

def parse_rules(string):
	rules = []
	for rule in string.split(','):
		if ':' in rule:
			check, dest = rule.split(':')
			rules.append(Rule(check, dest))
		else:
			rules.append(Rule(None, rule))
	return rules

def parse_part(string):
	fields = {}
	for key, value in [substring.split('=') for substring in string.split(',')]:
		fields[key] = int(value)
	return fields

def parse_input(filename):
	file = open(filename, 'r')
	lines = [line.strip() for line in file.readlines()]

	workflows = {}
	for line in lines:
		if len(line) == 0:
			break
		(workflow, rules) = line.split('{')
		rules = rules[0:-1]
		workflows[workflow] = parse_rules(rules)

	parts = []
	for line in lines[len(workflows) + 1:]:
		parts.append(parse_part(line[1:-1]))

	return workflows, parts

def evaluate(check, part):
	if check == None:
		return True

	field = check[0]
	comparison = check[1]
	value = int(check[2:])

	field_value = part[field]
	return field_value < value if comparison == '<' else field_value > value

def solve_1(filename):
	(workflows, parts) = parse_input(filename)

	xmas_sum = 0
	for part in parts:
		workflow = workflows['in']
		while workflow:
			for rule in workflow:
				if evaluate(rule.check, part):
					if rule.dest == 'A':
						xmas_sum += sum(part.values())
						workflow = None
					elif rule.dest == 'R':
						workflow = None
					else:
						workflow = workflows[rule.dest]
					break
	print(filename, 'xmas_sum', xmas_sum)

def acceptance(workflows, workflow_id, part_intervals):
	if workflow_id == 'A':
		return reduce(lambda prod, interval: prod * (interval[1] - interval[0] + 1), part_intervals.values(), 1)
	if workflow_id == 'R':
		return 0

	sum_acceptance = 0
	for rule in workflows[workflow_id]:
		if rule.check == None:
			sum_acceptance += acceptance(workflows, rule.dest, part_intervals)
			break

		field = rule.check[0]
		comparison = rule.check[1]
		value = int(rule.check[2:])

		interval = part_intervals[field]
		if comparison == '<':
			if interval[1] < value:
				sum_acceptance += acceptance(workflows, rule.dest, part_intervals)
			elif interval[0] <= value and value <= interval[1]:
				in_interval = (interval[0], value - 1)
				in_fields = part_intervals.copy()
				in_fields[field] = in_interval
				sum_acceptance += acceptance(workflows, rule.dest, in_fields)

				out_interval = (value, interval[1])
				part_intervals[field] = out_interval
		else: # comparison == '>'
			if interval[0] > value:
				sum_acceptance += acceptance(workflows, rule.dest, part_intervals)
			elif interval[0] <= value and value <= interval[1]:
				in_interval = (value + 1, interval[1])
				in_fields = part_intervals.copy()
				in_fields[field] = in_interval
				sum_acceptance += acceptance(workflows, rule.dest, in_fields)

				out_interval = (interval[0], value)
				part_intervals[field] = out_interval

	return sum_acceptance

def solve_2(filename):
	(workflows, _) = parse_input(filename)

	part_intervals = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
	print(filename, 'sum_acceptance', acceptance(workflows, 'in', part_intervals))

solve_1('19_sample.txt')
solve_1('19_input.txt')

solve_2('19_sample.txt')
solve_2('19_input.txt')
