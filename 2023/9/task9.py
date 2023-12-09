def next_number(numbers):
    return numbers[-1] + sum(solve_and_collect(numbers, -1))

def next_number2(numbers):
    first_numbers, diff = solve_and_collect(numbers, 0), 0
    for i in range(len(first_numbers) - 1, -1, -1):
        diff = first_numbers[i] - diff
    return numbers[0] - diff

def solve_and_collect(numbers, index):
    next_numbers, edge_numbers = numbers, []
    while any([n != 0 for n in next_numbers]):
        next_numbers = [next_numbers[i] - next_numbers[i-1] for i in range(1, len(next_numbers))]
        edge_numbers.append(next_numbers[index])
    return edge_numbers

def solve(f, part=1):
    reduce_func = next_number if part == 1 else next_number2
    answer = sum(reduce_func(numbers) for numbers in [[int(n) for n in line.split()] for line in f])
    print(answer)

with open("9.input") as f:
# with open("test9.txt") as f:
    solve(f, 2)
