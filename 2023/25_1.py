# https://adventofcode.com/2023/day/25

def parse_input(filename):
	file = open(filename, 'r')
	lines = file.readlines()
	graph = {}
	for line in [line.strip() for line in lines]:
		vertex_a, vertices = line.split(': ')
		for vertex_b in vertices.split(' '):
			graph.setdefault(frozenset({vertex_a}), {})[frozenset({vertex_b})] = 1
			graph.setdefault(frozenset({vertex_b}), {})[frozenset({vertex_a})] = 1
	return graph


def add_to_A(graph, A, vertex):
	A[0].add(vertex)
	A[1].pop(vertex, None)
	for edge, cost in graph[vertex].items():
		if edge not in A[0]:
			A[1][edge] = A[1].get(edge, 0) + cost

def merge_vertices(graph, vertex_a, vertex_b):
	vertex_ab = frozenset.union(vertex_a, vertex_b)
	edges_a = graph[vertex_a]
	edges_b = graph[vertex_b]

	new_edges = {}
	for vertex_c in set(edges_a.keys()).union(edges_b.keys()):
		graph[vertex_c].pop(vertex_a, None)
		graph[vertex_c].pop(vertex_b, None)

		if vertex_c == vertex_a or vertex_c == vertex_b:
			continue

		new_weight = edges_a.get(vertex_c, 0) + edges_b.get(vertex_c, 0)
		new_edges[vertex_c] = new_weight
		graph[vertex_c][vertex_ab] = new_weight

	graph.pop(vertex_a)
	graph.pop(vertex_b)
	graph[vertex_ab] = new_edges

def minimum_cut_phase(graph):
	A = (set(), {})

	a = list(graph.keys())[0]
	add_to_A(graph, A, a)
	# a = frozenset('2')
	# add_to_A(graph, A, frozenset('2'))

	one_before_last_vertex = None
	last_vertex = a
	cut_weight = None
	while len(A[0]) < len(graph):
		vertex = max(A[1].keys(), key=lambda key: A[1][key])
		cut_weight = A[1][vertex]
		if DEBUG: print('cutting', vertex, 'w:', cut_weight)

		add_to_A(graph, A, vertex)
		if DEBUG: print('A', A[0], '->', A[1], 'w:')

		one_before_last_vertex = last_vertex
		last_vertex = vertex

	if DEBUG: print('merging', one_before_last_vertex, 'and', last_vertex, 'weight:', cut_weight)
	merge_vertices(graph, one_before_last_vertex, last_vertex)

	if DEBUG:
		for vertex, edges in graph.items(): print(vertex, '->', edges)

	return (cut_weight, last_vertex)

def solve(filename):
	global DEBUG
	graph = parse_input(filename)
	# https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm#Example
	# https://dl.acm.org/doi/pdf/10.1145/263867.263872
	# graph = {}
	# graph[frozenset('1')] = {frozenset({'2'}): 2, frozenset({'5'}): 3}
	# graph[frozenset('2')] = {frozenset({'1'}): 2, frozenset({'5'}): 2, frozenset({'6'}): 2, frozenset({'3'}): 3}
	# graph[frozenset('3')] = {frozenset({'2'}): 3, frozenset({'7'}): 2, frozenset({'4'}): 4}
	# graph[frozenset('4')] = {frozenset({'3'}): 4, frozenset({'7'}): 2, frozenset({'8'}): 2}
	# graph[frozenset('5')] = {frozenset({'1'}): 3, frozenset({'2'}): 2, frozenset({'6'}): 3}
	# graph[frozenset('6')] = {frozenset({'5'}): 3, frozenset({'2'}): 2, frozenset({'7'}): 1}
	# graph[frozenset('7')] = {frozenset({'6'}): 1, frozenset({'3'}): 2, frozenset({'4'}): 2, frozenset({'8'}): 3}
	# graph[frozenset('8')] = {frozenset({'7'}): 3, frozenset({'4'}): 2}
	if DEBUG:
		for vertex, edges in graph.items(): print(vertex, '->', edges)

	graph_length = len(graph)
	minimum_cut = (float('inf'), None)
	iterations = 0
	while len(graph) > 1 and minimum_cut[0] != 3:
		minimum_cut = min(minimum_cut, minimum_cut_phase(graph), key=lambda cut: cut[0])
		iterations += 1

	print(filename, 'minimum_cut', minimum_cut, 'product', (graph_length - len(minimum_cut[1])) * len(minimum_cut[1]))

DEBUG = False
solve('25_sample.txt')
solve('25_input.txt')
