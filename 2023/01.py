# https://adventofcode.com/2023/day/1

def find_digit(line, last = False):
	for index, char in enumerate(line if not last else reversed(line)):
		if char.isdigit():
			return index if not last else len(line) - index - 1, char
	return None

def find_number(line, last = False):
	numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
	if last:
		indexes = [line.rfind(number) for number in numbers]
		found = None
		for number, index in enumerate(indexes):
			if index > -1 and (found is None or index > found[0]):
				found = index, str(number)
		return found
	else:
		indexes = [line.find(number) for number in numbers]
		found = None
		for number, index in enumerate(indexes):
			if index > -1 and (found is None or index < found[0]):
				found = index, str(number)
		return found

# sum = 0
# file = open('01.in', 'r')
# for line in file.readlines():
# 	index, first = find_digit(line)
# 	index, last = find_digit(line, last = True)
# 	print(first, last)

# 	number = int(first + last)
# 	print(number)

# 	sum += number
# print("todal sum:", sum)

sum = 0
file = open('01.in', 'r')
for line in file.readlines():
	print()
	print()
	print(line)

	first_digit = find_digit(line)
	first_number = find_number(line)
	print("first_digit", first_digit)
	print("first_number", first_number)
	first = first_digit
	if first_number is not None and first_number[0] < first_digit[0]:
		first = first_number
	print("first", first)
	
	last_digit = find_digit(line, last = True)
	last_number = find_number(line, last = True)
	print("last_digit", last_digit)
	print("last_number", last_number)
	last = last_digit
	if last_number is not None and last_number[0] > last_digit[0]:
		last = last_number
	print("last", last)

	number = int(first[1] + last[1])
	print(number)

	sum += number
print("todal sum:", sum)
