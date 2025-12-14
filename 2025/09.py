# https://adventofcode.com/2025/day/9

from PIL import Image, ImageDraw

def parse_input(filename):
	file = open(filename, 'r')
	tiles = []
	for line in [line.strip() for line in file.readlines()]:
		tiles.append(tuple([int(num) for num in line.split(',')]))
	return tiles

def solve_1(filename):
	tiles = parse_input(filename)

	max_area = -1
	for i, tile_a in enumerate(tiles):
		for tile_b in tiles[i + 1:]:
			area = (abs(tile_a[0] - tile_b[0]) + 1) * (abs(tile_a[1] - tile_b[1]) + 1)
			if area > max_area:
				max_area = area

	print('max_area', max_area)

# https://www.xjavascript.com/blog/check-if-polygon-is-inside-a-polygon/#algorithm
def is_inside(hor_lines, ver_lines, x, y):
	for line in hor_lines:
		if y == line[0][1] and x >= line[0][0] and x <= line[1][0]:
			return True
	for line in ver_lines:
		if x == line[0][0] and y >= line[0][1] and y <= line[1][1]:
			return True

	inside = False
	for line in ver_lines:
		((xi, yi), (xj, yj)) = line
		# Check if the edge crosses the horizontal ray (y = point.y)
		# First, ensure the edge straddles the ray's y-coordinate
		if (yi > y) != (yj > y):
			# Compute x-intersection of the edge with the ray
			x_intersect = ( (y - yi) * (xj - xi) ) / (yj - yi) + xi
			# If the intersection is to the right of the point, flip "inside"
			if x < x_intersect:
				inside = not inside
	
	return inside

def intersects_ver(ver_lines, y, x_a, x_b):
	for line in ver_lines:
		if y > line[0][1] and y < line[1][1] and x_a < line[0][0] and x_b > line[0][0]:
			return True
	return False

def intersects_hor(hor_lines, x, y_a, y_b):
	for line in hor_lines:
		if x > line[0][0] and x < line[1][0] and y_a < line[0][1] and y_b > line[0][1]:
			return True
	return False

def is_all_red_or_green(hor_lines, ver_lines, tile_a, tile_b):
	(min_x, max_x) = sorted([tile_a[0], tile_b[0]])
	(min_y, max_y) = sorted([tile_a[1], tile_b[1]])

	if not is_inside(hor_lines, ver_lines, min_x, min_y) \
		or not is_inside(hor_lines, ver_lines, min_x, max_y) \
		or not is_inside(hor_lines, ver_lines, max_x, min_y) \
		or not is_inside(hor_lines, ver_lines, max_x, max_y):
		return False

	if intersects_ver(ver_lines, tile_a[1], min_x, max_x) \
		or intersects_ver(ver_lines, tile_b[1], min_x, max_x) \
		or intersects_hor(hor_lines, tile_a[0], min_y, max_y) \
		or intersects_hor(hor_lines, tile_b[0], min_y, max_y):
		return False

	return True

def saveImages(filename, lines, rect, scale):
	width = int(max(map(lambda line: line[1][0], lines)) / scale) + int(min(map(lambda line: line[0][0], lines)) / scale) + 1
	height = int(max(map(lambda line: line[1][1], lines)) / scale) + int(min(map(lambda line: line[0][1], lines)) / scale) + 1

	grid = Image.new('RGBA', (width, height), (0, 0, 0, 0))
	gridDraw = ImageDraw.Draw(grid)  
	for line in lines:
		gridDraw.line((int(line[0][0]/scale), int(line[0][1]/scale), int(line[1][0]/scale), int(line[1][1]/scale)), (0, 0, 0, 255))

	rectImg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
	rectDraw = ImageDraw.Draw(rectImg)  
	rectDraw.rectangle([int(rect[0][0]/scale), int(rect[0][1]/scale), int(rect[1][0]/scale), int(rect[1][1]/scale)], (255, 0, 255, 127))

	grid.paste(rectImg, mask=rectImg)
	grid.save(filename + '.png')

def solve_2(filename, scale = 1):
	tiles = parse_input(filename)

	hor_lines = []
	ver_lines = []
	for i, tile in enumerate(tiles):
		tile_n = tiles[(i + 1) % len(tiles)]
		if tile[0] == tile_n[0]:
			ver_lines.append(((tile[0], min(tile[1], tile_n[1])), (tile[0], max(tile[1], tile_n[1]))))
		elif tile[1] == tile_n[1]:
			hor_lines.append(((min(tile[0], tile_n[0]), tile[1]), (max(tile[0], tile_n[0]), tile[1])))
		else:
			raise ValueError('Oh no')

	max_area = -1
	max_tiles = None
	for i, tile_a in enumerate(tiles):
		for tile_b in tiles[i + 1:]:
			area = (abs(tile_a[0] - tile_b[0]) + 1) * (abs(tile_a[1] - tile_b[1]) + 1)
			if area > max_area and is_all_red_or_green(hor_lines, ver_lines, tile_a, tile_b):
				max_area = area
				max_tiles = [tile_a, tile_b]

	saveImages(filename, hor_lines + ver_lines, max_tiles, scale)
	print('max_area', max_area)

solve_1('09_sample.txt') # 50
solve_1('09_input.txt') # 4774877510

solve_2('09_sample.txt') # 24
solve_2('09_input.txt', 10) # 1560475800
