from typing import Any, Dict, List, Tuple

import numpy as np

N, S, E, W = 1, 2, 4, 8

DX: Dict[int, int] = {E: 1, W: -1, N: 0, S: 0}
DY: Dict[int, int] = {E: 0, W: 0, N: -1, S: 1}

OPPOSITE: Dict[int, int] = {E: W, W: E, N: S, S: N}


class DisjointSet:
    class Node:
        def __init__(self, value, parent):
            self.value = value
            self.parent = parent

    def __init__(self, nodes):
        self._node_map: Dict = {}

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
        def generate(grid_shape: Tuple[int, int], seed: int = 0) -> np.ndarray:
            def neighbor(r: int, c: int, direction: int) -> Tuple[int, int]:
                return r + DY[direction], c + DX[direction]

            def compute_maze_shape(rows: int, cols: int) -> Tuple[int, int]:
                return rows * 2 + 1, cols * 2 + 1

            np.random.seed(seed)

            rows, cols = grid_shape

            nodes: List[Tuple[int, int]] = [(r, c) for r in range(int(rows)) for c in range(int(cols))]

            disjoint_set: DisjointSet = DisjointSet(nodes)

            internal_edges: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
            for r, c in nodes:
                if r:
                    internal_edges.append((neighbor(r, c, N), (r, c)))
                if c:
                    internal_edges.append((neighbor(r, c, W), (r, c)))

            maze: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
            for edge in sorted(internal_edges, key=lambda _: np.random.random()):
                node_a, node_b = edge
                if disjoint_set.find_parent(node_a) != disjoint_set.find_parent(node_b):
                    disjoint_set.union(node_a, node_b)
                    maze.append(edge)

            maze_shape: Tuple[int, int] = compute_maze_shape(rows, cols)
            maze_map: np.ndarray = np.zeros(maze_shape, dtype=np.uint8)
            for edge in maze:
                (a_r, a_c), (b_r, b_c) = edge
                min_x, min_y = compute_maze_shape(min(a_r, b_r), min(a_c, b_c))
                max_x, max_y = compute_maze_shape(max(a_r, b_r), max(a_c, b_c))
                maze_map[min_x: max_x + 1, min_y: max_y + 1] = 1

            return maze_map


class Map:
    @staticmethod
    def generate(shape: Tuple[int, int], generator: Any = Maze.Kruskal, seed: int = 0) -> np.ndarray:
        return generator.generate(shape, seed)
