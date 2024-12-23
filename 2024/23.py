# https://adventofcode.com/2024/day/23

from collections import defaultdict
from itertools import combinations

def parse_input(filename):
	file = open(filename, 'r')
	return [tuple(line.strip().split('-')) for line in file.readlines()]

def are_connected(connections, a, b):
	return (a, b) in connections or (b, a) in connections

def add_to_lans(connections, pc_lans, a, b):
	for lan in pc_lans[a]:
		if all(are_connected(connections, b, lan_pc) for lan_pc in lan):
			lan.add(b)
	pc_lans[a].append(set([a, b]))

def solve(filename):
	connections = set(parse_input(filename))

	pc_lans = defaultdict(list)
	for a, b in connections:
		add_to_lans(connections, pc_lans, a, b)
		add_to_lans(connections, pc_lans, b, a)

	# part 1
	t_lans = set()
	for pc, lans in pc_lans.items():
		for lan in lans:
			if len(lan) < 3:
				continue
			for p in [p for p in lan if p[0] == 't']:
				lan_minus_p = set(lan)
				lan_minus_p.remove(p)
				for sub_lan in combinations(lan_minus_p, 2):
					t_lans.add(frozenset(set([p]) | set(sub_lan)))
	print('len(t_lans)', len(t_lans))

	# part 2
	largest_lan = None
	for lans in pc_lans.values():
		for lan in lans:
			if largest_lan == None or len(lan) > len(largest_lan):
				largest_lan = lan
	print('largest_lan', largest_lan)
	print('password', ','.join(sorted(largest_lan)))


solve('23_sample.txt') # 7		co,de,ka,ta
solve('23_input.txt') # 1194	bd,bu,dv,gl,qc,rn,so,tm,wf,yl,ys,ze,zr
