import random

from collections import deque
import heapq

class Grid:

    graph : dict
    goal: int
    start: int

    def __init__(self, size : int = 20, nb_walls : int = 3, wall_size : tuple[int,int] = (1, 5)):
        self.size = size
        self.nb_walls = nb_walls
        self.min_wsize, self.max_wsize = wall_size

        self.generate()

    def generate(self):
        self.graph = {}

        for i in range(self.size):
            for j in range(self.size):
                self.graph[(j,i)] = set()

                if i > 0:
                    self.graph[(j,i)].add((j,i-1))
                if i < self.size - 1:
                    self.graph[(j,i)].add((j,i+1))
                if j > 0:
                    self.graph[(j,i)].add((j-1,i))
                if j < self.size - 1:
                    self.graph[(j,i)].add((j+1,i))


        for _ in range(self.nb_walls):
            vertical = random.randint(0,1) == 1
            sommets = list(self.graph.keys())
            (x,y) = random.choice(sommets)
            wall_size = random.randint(self.min_wsize, self.max_wsize)

            alternate = [(1,0), (-1,0)]
            if vertical:
                n_alternate = [(ty,tx) for (tx,ty) in alternate]
                alternate = n_alternate
            l = [(x,y) for _ in range(len(alternate))]
            for (_x,_y) in self.graph[(x,y)]:
                self.graph[(_x,_y)].remove((x,y))
            self.graph.pop((x,y))
            wall_size -= 1
            while(wall_size > 0):
                for i in range(len(alternate)):
                    (nx,ny) = l[i]
                    (dx,dy) = alternate[i]

                    nx += dx
                    ny += dy

                    if (nx,ny) in self.graph:
                        for (_x,_y) in self.graph[(nx,ny)]:
                            self.graph[(_x,_y)].remove((nx,ny))
                        self.graph.pop((nx,ny))
                        wall_size -= 1
                        if(wall_size <= 0):
                            break

                    l[i] = (nx,ny)
                if len(self.graph) == 0:
                    break
        if len(self.graph) == 0:
            return
        sommets = list(self.graph.keys())
        self.start = random.choice(sommets)
        sommets.remove(self.start)
        if(len(sommets) == 0):
            self.goal = self.start
        else:
            self.goal = random.choice(sommets)

    def initial(self) -> int:
        return self.start

    def successeurs(self, sommet : tuple[int, int]) -> set[tuple[int,int]]:
        return self.graph[sommet]
    
    def is_goal(self, sommet : tuple[int, int]) -> bool:
        return sommet == self.goal
    
    def heuristic(self, sommet: tuple[int, int]) -> float:
        """Distance de Manhattan basée sur les positions 2D."""
        x1, y1 = sommet
        x2, y2 = self.goal
        return abs(x1 - x2) + abs(y1 - y2)
     
def bfs_grid(grid: Grid):
    start = grid.initial()
    goal = grid.goal

    queue = deque([start])
    visited = set([start])
    explored = 0

    while queue:
        node = queue.popleft()
        explored += 1

        if node == goal:
            return True, len(visited)

        for neighbor in grid.successeurs(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False, len(visited)



def dfs_grid(grid: Grid):
    start = grid.initial()
    goal = grid.goal

    stack = [start]
    visited = set([start])
    explored = 0

    while stack:
        node = stack.pop()
        explored += 1

        if node == goal:
            return True, len(visited)

        for neighbor in grid.successeurs(node):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return False, len(visited)

def dijkstra_grid(grid: Grid):
    start = grid.initial()
    goal = grid.goal

    dist = {node: float('inf') for node in grid.graph}
    parents = {node: None for node in grid.graph}

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

        for neighbor in grid.successeurs(node):
            new_cost = current_cost + 1

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parents[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return False, float('inf'), explored


def astar(grid: Grid):
    start = grid.initial()
    goal = grid.goal

    pq = [(grid.heuristic(start), 0, start)]
    dist = {node: float('inf') for node in grid.graph}
    dist[start] = 0
    visited = set()

    explored = 1

    while pq:
        f_score, g_score, pos = heapq.heappop(pq)
        
        if pos in visited:
            continue
            
        visited.add(pos)

        if pos == goal:
            return True, g_score, explored

        for voisin in grid.successeurs(pos):
            if voisin in visited:
                continue
            explored += 1
            new_cost = g_score + 1

            if new_cost < dist[voisin]:
                dist[voisin] = new_cost
                f_cost = new_cost + grid.heuristic(voisin)
                heapq.heappush(pq, (f_cost, new_cost, voisin))

    return False, float('inf'), explored


def search_idastar(grid: Grid, path, g, bound, explored):
    node = path[-1]
    explored[0] += 1

    f = g + grid.heuristic(node)

    if f > bound:
        return False, f

    if grid.is_goal(node):
        return True, g

    min_bound = float('inf')

    for succ in grid.successeurs(node):
        if succ in path:
            continue
        
        path.append(succ)
        found, result = search_idastar(grid, path, g + 1, bound, explored)

        if found:
            return True, result

        if result < min_bound:
            min_bound = result

        path.pop()

    return False, min_bound


def ida_star(grid: Grid):
    start = grid.initial()

    bound = grid.heuristic(start)
    explored = [0]
    max_depth = len(grid.graph)

    while True:
        path = [start]
        found, result = search_idastar(grid, path, 0, bound, explored)

        if found:
            return True, result, explored[0]

        if result == float('inf'):
            return False, float('inf'), explored[0]

        bound = result
    
        if bound > max_depth * 2:
            return False, float('inf'), explored[0]
