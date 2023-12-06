from math import sqrt

def find_best_times(T, dist):
    sqrt_d = sqrt(T * T - 4 * dist)
    t1, t2 = round(T - sqrt_d) >> 1, round(T + sqrt_d) >> 1
    t1 += 1 if not check(t1, T, dist) else 0  # We need to check real boundary, as we operate INTs, not real numbers
    t2 -= 1 if not check(t2, T, dist) else 0
    return t2 - t1 + 1

def check(t, T, dist):
    return (T - t) * t > dist

def part1(f):
    times = [int(n) for n in to_numbers(next(f))]
    distances = [int(n) for n in to_numbers(next(f))]
    res = 1
    for t, d in zip(times, distances):
        res *= find_best_times(t, d)
    print(res)

def part2(f):
    times = int(''.join(to_numbers(next(f))))
    distances = int(''.join(to_numbers(next(f))))
    print(find_best_times(times, distances))

def to_numbers(line: str):
    return line.split(":")[1].split()

# with open("test6.txt") as f:
with open("6.input") as f:
    # part1(f)
    part2(f)
