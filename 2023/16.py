# https://adventofcode.com/2023/day/16

from dataclasses import dataclass

@dataclass(eq = True, frozen = True)
class Beam:
	position: tuple # (i, j)
	direction: tuple # (di, dj)

	def is_inside(self, grid):
		return self.position[0] >= 0 and self.position[0] < len(grid) and self.position[1] >= 0 and self.position[1] < len(grid[0])

	def advance(self):
		return self.advance_by(self.direction)

	def advance_by(self, direction):
		return Beam((self.position[0] + direction[0], self.position[1] + direction[1]), direction)

	def is_direction_horizontal(self):
		return self.direction[1] != 0

	def is_direction_vertical(self):
		return self.direction[0] != 0

	def split_horizontally(self):
		return (Beam((self.position[0], self.position[1] - 1), (0, -1)), Beam((self.position[0], self.position[1] + 1), (0, 1)))

	def split_vertically(self):
		return (Beam((self.position[0] - 1, self.position[1]), (-1, 0)), Beam((self.position[0] + 1, self.position[1]), (1, 0)))

def calculate_energized(grid, beam):
	beams = [beam]
	energized = set()

	iterations = 0
	while beams:
		for b, beam in reversed(list(enumerate(beams))):
			beams.pop(b)
			if not beam.is_inside(grid) or beam in energized:
				continue
			energized.add(beam)
			tile = grid[beam.position[0]][beam.position[1]]
			if tile == '.':
				beams.append(beam.advance())
			elif tile == '-':
				if beam.is_direction_horizontal():
					beams.append(beam.advance())
				else:
					beams.extend(beam.split_horizontally())
			elif tile == '|':
				if beam.is_direction_vertical():
					beams.append(beam.advance())
				else:
					beams.extend(beam.split_vertically())
			elif tile == '/':
				beams.append(beam.advance_by((beam.direction[1] * -1, beam.direction[0] * -1)))
			elif tile == '\\':
				beams.append(beam.advance_by((beam.direction[1], beam.direction[0])))
		iterations += 1

	energized_position = set()
	for energy in energized:
		energized_position.add(energy.position)
	energized = len(energized_position)
	# print('iterations', iterations, 'energized', energized)
	return len(energized_position)

def solve_1(filename):
	file = open(filename, 'r')
	grid = [[char for char in line.strip()] for line in file.readlines()]

	energized = calculate_energized(grid, Beam((0, 0), (0, 1)))
	print(filename, 'energized', energized)

def solve_2(filename):
	file = open(filename, 'r')
	grid = [[char for char in line.strip()] for line in file.readlines()]

	energized = 0
	for i in range(len(grid)):
		energized = max(energized, calculate_energized(grid, Beam((i, 0), (0, 1))))
		energized = max(energized, calculate_energized(grid, Beam((i, len(grid[0]) - 1), (0, -1))))
	for j in range(len(grid[0])):
		energized = max(energized, calculate_energized(grid, Beam((0, j), (1, 0))))
		energized = max(energized, calculate_energized(grid, Beam((len(grid) - 1, j), (-1, 0))))
	print(filename, 'max energized', energized)

solve_1('16_sample.txt')
solve_1('16_input.txt')

solve_2('16_sample.txt')
solve_2('16_input.txt')
