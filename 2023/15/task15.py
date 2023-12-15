def fancy_hash(s: str) -> int:
    h = 0
    for c in s:
        h = 17 * (h + ord(c)) % 256
    return h

class FancyMap:
    def __init__(self) -> None:
        self.boxes = [Box(i) for i in range(256)]

    def execute(self, operation: str):
        if "=" in operation:
            # Add
            label, focal_len = operation.split("=")
            box_number, focal_len = fancy_hash(label), int(focal_len)
            self.put(box_number, label, focal_len)
        else:
            # Remove
            label = operation.replace("-", "")
            box_number = fancy_hash(label)
            self.remove(box_number, label)

    def remove(self, box: int, label: str):
        self.boxes[box].remove(label)

    def put(self, box: int, label: str, focal_len: int):
        self.boxes[box].put(label, focal_len)

    def focusing_power(self):
        return sum([box.focusing_power() for box in self.boxes])

class Node:
    def __init__(self, label: str, focal_len: int) -> None:
        self.label = label
        self.focal_len = focal_len
        self.prev = None
        self.next = None

class Box:
    def __init__(self, number: int) -> None:
        self.number = number
        self.label2node = {}
        self.first = Node("santinel", -1)
        self.last = self.first

    def put(self, label: str, focal_len: int):
        if label in self.label2node:
            node = self.label2node[label]
            node.focal_len = focal_len
            return
        node = Node(label, focal_len)
        self.label2node[label] = node
        self.last.next = node
        node.prev = self.last
        self.last = node

    def remove(self, label: str):
        if label not in self.label2node:
            return
        node = self.label2node[label]
        node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.last = node.prev
        del self.label2node[label]

    def focusing_power(self):
        node, index, total = self.first, 1, 0
        while node.next:
            node = node.next
            total += index * node.focal_len
            index += 1
        return (self.number + 1) * total

# with open("test15.txt") as f:
with open("15.input") as f:
    line = f.readline().strip()
    f_map = FancyMap()
    for command in line.split(","):
        f_map.execute(command)
    print(f_map.focusing_power())
    # hsh = sum([fancy_hash(s) for line in f for s in line.strip().split(",")])

