import numpy as np


class Direction:
    N, S, E, W = 1, 2, 4, 8

    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}

    OPPOSITE = {E: W, W: E, N: S, S: N}


class DisjointSet:
    class Node:
        def __init__(self, value, parent):
            self.value = value
            self.parent = parent

    def __init__(self, nodes):
        self._node_map = {}

        for i, value in enumerate(nodes):
            n = DisjointSet.Node(value, i)
            self._node_map[value] = n

    def find_parent(self, node):
        return self.find_node(node).parent

    def find_node(self, node):
        if type(self._node_map[node].parent) is int:
            return self._node_map[node]
        else:
            parent_node = self.find_node(self._node_map[node].parent.value)
            self._node_map[node].parent = parent_node
            return parent_node

    def union(self, node_a, node_b):
        parent_a = self.find_node(node_a)
        parent_b = self.find_node(node_b)
        if parent_a.parent != parent_b.parent:
            parent_a.parent = parent_b


class Maze:
    class Kruskal:
        @staticmethod
        def generate(grid_shape, seed=0):
            def neighbor(r, c, direction):
                return (r + Direction.DY[direction], c + Direction.DX[direction])

            def compute_maze_shape(rows, cols):
                return (rows * 2 + 1, cols * 2 + 1)

            np.random.seed(seed)

            rows, cols = grid_shape

            nodes = [(r, c) for r in range(rows) for c in range(cols)]

            disjoint_set = DisjointSet(nodes)

            internal_edges = []
            for r, c in nodes:
                if r:
                    internal_edges.append((neighbor(r, c, Direction.N), (r, c)))
                if c:
                    internal_edges.append((neighbor(r, c, Direction.W), (r, c)))

            maze = []
            for edge in sorted(internal_edges, key=lambda _: np.random.random()):
                node_a, node_b = edge
                if disjoint_set.find_parent(node_a) != disjoint_set.find_parent(node_b):
                    disjoint_set.union(node_a, node_b)
                    maze.append(edge)

            maze_shape = compute_maze_shape(rows, cols)
            maze_map = np.zeros(maze_shape, dtype=np.uint8)
            for edge in maze:
                (a_r, a_c), (b_r, b_c) = edge
                min_x = min(a_r, b_r) * 2 + 1
                max_x = max(a_r, b_r) * 2 + 1
                min_y = min(a_c, b_c) * 2 + 1
                max_y = max(a_c, b_c) * 2 + 1
                maze_map[min_x : max_x + 1, min_y : max_y + 1] = 1

            return maze_map


class Map:
    @staticmethod
    def generate(shape, generator=Maze.Kruskal, seed=0):
        return generator.generate(shape, seed)
