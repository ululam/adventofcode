from math import sqrt, floor, ceil

def find_best_times(T, dist):
    t1 = (T - sqrt(T*T - 4*dist))/2
    t2 = (T + sqrt(T*T - 4*dist))/2
    t1, t2 = int(floor(t1)), int(ceil(t2))
    t1 += 1 if not check(t1, T, dist) else 0
    t2 -= 1 if not check(t2, T, dist) else 0
    return t2 - t1 + 1

def check(t, T, D):
    return (T - t) * t > D

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
