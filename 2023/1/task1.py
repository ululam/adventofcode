digits = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}

self_digits = {str(v): v for v in digits.values()}
digits = dict(list(digits.items()) + list(self_digits.items()))


def _min_index(s, k):
    i = s.find(k)
    return i if i >= 0 else 100_000


def find_left(s: str):
    return min([(_min_index(s, k), v) for k, v in digits.items()], key=lambda t: t[0])[1]


def find_right(s: str):
    return max([(s.rfind(k), v) for k, v in digits.items()], key=lambda t: t[0])[1]


summa = 0
with open("example1.2.txt") as file_in:
    for line in file_in:
        summa += 10 * find_left(line) + find_right(line)

print(summa)
