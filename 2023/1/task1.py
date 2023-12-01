digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

self_digits = {str(v): v for v in digits.values()}
digits = dict(list(digits.items()) + list(self_digits.items()))


def find_left(s: str):
    index, digit = 100_000, 0
    for k, v in digits.items():
        i = s.find(k)
        if -1 < i < index:
            digit = v
            index = i
    return digit


def find_right(s: str):
    index, digit = -1, 0
    for k, v in digits.items():
        i = s.rfind(k)
        if i > index:
            digit = v
            index = i
    return digit


summa = 0
with open("1/1.txt") as file_in:
    for line in file_in:
        summa += 10 * find_left(line) + find_right(line)

print(summa)
