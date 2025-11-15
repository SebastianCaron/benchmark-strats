import random

from collections import deque
import heapq


class Graph:

    graph : dict
    goal: int
    start: int

    def __init__(self, size : int = 20, is_oriented : bool = True, weight : tuple[int, int] = (1,1)):
        self.size = size
        self.is_oriented = is_oriented
        self.min_weigth, self.max_weigth = weight

        self.generate()

    def generate(self):
        self.graph = {}

        for i in range(self.size):
            self.graph[i] = {}

        sommets = list(self.graph.keys())
        for i in self.graph:
            neighbors = random.choices(sommets, k = min(self.size, random.randint(0, self.size-1)))

            for j in neighbors:
                self.graph[i][j] = random.randint(self.min_weigth, self.max_weigth)
                if not self.is_oriented:
                    self.graph[j][i] = random.randint(self.min_weigth, self.max_weigth)
        
        self.start = random.randint(0, self.size - 1)
        self.goal = random.randint(0, self.size - 1)
        if self.size <= 1:
            return
        while(self.goal == self.start):
            self.goal = random.randint(0, self.size - 1)

    def initial(self) -> int:
        return self.start

    def successeurs(self, sommet : int) -> dict[int, int]:
        return self.graph[sommet]
    
    def is_goal(self, sommet) -> bool:
        return sommet == self.goal
     



def bfs(graph: Graph):
    start = graph.initial()
    goal = graph.goal

    queue = deque([start])
    visited = set([start])
    explored = 0

    while queue:
        node = queue.popleft()
        explored += 1

        if node == goal:
            return True, explored

        for neighbor in graph.successeurs(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False, explored



def dfs(graph: Graph):
    start = graph.initial()
    goal = graph.goal

    stack = [start]
    visited = set([start])
    explored = 0

    while stack:
        node = stack.pop()
        explored += 1

        if node == goal:
            return True, explored

        for neighbor in graph.successeurs(node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return False, explored



def dijkstra(graph: Graph):
    start = graph.initial()
    goal = graph.goal

    dist = {node: float('inf') for node in graph.graph}
    parents = {node: None for node in graph.graph}

    dist[start] = 0

    heap = [(0, start)]
    explored = 0

    while heap:
        current_cost, node = heapq.heappop(heap)
        explored += 1

        if node == goal:
            return True, current_cost, explored

        if current_cost > dist[node]:
            continue

        for neighbor, weight in graph.successeurs(node).items():
            new_cost = current_cost + weight

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parents[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return False, float('inf'), explored

