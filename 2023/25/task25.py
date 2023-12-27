from collections import defaultdict, Counter, deque
from queue import Queue


def read_input(f):
    graph = defaultdict(list)
    for line in f:
        left_right = line.strip().split(":")
        left = left_right[0]
        for right in left_right[1].split():
            graph[left].append(right)
            graph[right].append(left)
    return graph

def find_paths(graph):
    paths = {}
    vertices = list(graph.keys())
    for i in range(len(vertices) - 1):
        for j in range(i + 1, len(vertices)):
            paths[vertices[i], vertices[j]] = find_shortest_path(vertices[i], vertices[j], graph)
    return paths

def calc_clusters(graph):
    q = deque()
    v0 = list(graph.keys())[0]
    q.append(v0)
    visited = set()
    while q:
        v = q.popleft()
        if v in visited:
            continue
        visited.add(v)
        for next_v in graph[v]:
            q.append(next_v)

    c1 = len(visited)
    c2 = len(graph.keys()) - c1
    return c1 * c2

dp = {}
def find_shortest_path(v1, v2, graph):
    q = Queue()
    q.put(v1)
    came_from = {}
    while q:
        v = q.get()
        if v == v2:
            break
        for next_v in graph[v]:
            if next_v not in came_from:
                q.put(next_v)
                came_from[next_v] = v
    v, path = v2, [v2]
    while v != v1:
        v = came_from[v]
        path.append(v)
    return path

with open("test25.txt") as f:
# with open("25.input") as f:
    g = read_input(f)
    paths = find_paths(g)
    all_paths = []
    for p in paths.values():
        p2 = []
        for i in range(len(p) - 1):
            p2.append(f"{' - '.join(sorted([p[i], p[i+1]]))}")
        all_paths += p2
    c = Counter(all_paths)
    for arc in c.most_common(3):
        vertices = arc[0].split(" - ")
        g[vertices[0]].remove(vertices[1])
        g[vertices[1]].remove(vertices[0])

    answer = calc_clusters(g)
    print(answer)
