class Node:
    def __init__(self, name: str, left, right) -> None:
        self.name, self.left, self.right = name, left, right

def solve(f):
    name_nodes, a_nodes = {}, []
    # First line is instructions
    directions = next(f).strip()
    next(f) # skip empty line
    for line in f:
        line = line.strip()
        name = line.split(" = ")[0]
        # if name == "AAA":             # Part 1
        if name.endswith("A"):          # Part 2
            a_nodes.append(name)
        left, right = line.replace("(", "").replace(")", "").split(" = ")[1].split(", ")
        name_nodes[name] = Node(name, left, right)
    counters = []
    for a_node in a_nodes:
        counter, dir_index = 0, 0
        while not a_node.endswith("Z"):
            direct = directions[dir_index]
            a_node = name_nodes[a_node].left if direct == 'L' else name_nodes[a_node].right
            dir_index += 1 if dir_index < len(directions)-1 else -dir_index
            counter += 1
        counters.append(counter)
    from math import lcm
    print(lcm(*counters))

def is_over(nodes: list[str]) -> bool:
    return len([n for n in nodes if not n.endswith("Z")]) == 0

with open("8.input") as f:
# with open("test8.txt") as f:
# with open("test8.1.txt") as f:
# with open("test8.2.txt") as f:
    solve(f)
