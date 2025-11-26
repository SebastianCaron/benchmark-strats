from collections import deque, defaultdict
import heapq

class Hanoi:

    def __init__(self, size = 5):
        self.size = size
        self.piles = [[] for _ in range(3)]
        self.piles[0] = [i for i in range(1, self.size)]
        

    def copy(self) -> "Hanoi":
        res = Hanoi(self.size)
        for i in range(len(self.piles)):
            res.piles[i] = self.piles[i].copy()
        return res

    def play(self, start : int, end : int):
        if not self.can_play(start, end):
            return self
        k = self.piles[start].pop()
        self.piles[end].append(k)
        return self

    def can_play(self, start : int, end : int):
        if(len(self.piles[start]) == 0):
            return False
        if(len(self.piles[end]) == 0):
            return True
        return (self.piles[start][-1] < self.piles[end][-1])
    
    def successors(self) -> dict[tuple[int, int], "Hanoi"]:
        res = {}
        coups = [0, 1, 2]
        for i in coups:
            for j in coups:
                if j != i and self.can_play(i, j):
                    res[(i, j)] = self.copy().play(i, j)
        return res
    
    def is_final(self):
        ldisque = self.size + 1
        for i in range(1, ldisque):
            if(self.piles[i] != ldisque - i):
                return False
        return True

    def __str__(self):
        return str(self.piles)
    
    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, value):
        if isinstance(value, Hanoi) and self.piles == value.piles:
            return True
        return False

    def __gt__(self, other):
        return False

    def __lt__(self, other):
        return False


def bfs_hanoi(hanoi : Hanoi):
    start = hanoi

    queue : deque[Hanoi] = deque([start])
    visited : set[Hanoi] = set([start])
    explored = 0

    while queue:
        node = queue.popleft()
        explored += 1

        if node.is_final():
            return True, explored

        for neighbor in node.successors().values():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False, explored

def dfs_hanoi(hanoi: Hanoi):
    start = hanoi
    stack : list[Hanoi] = [start]
    visited : set[Hanoi] = set([start])
    explored = 0

    while stack:
        node = stack.pop()
        explored += 1

        if node.is_final():
            return True, explored

        for neighbor in node.successors().values():
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return False, explored

def dijkstra_hanoi(start : Hanoi):
    dist = defaultdict(lambda : float('inf'))
    parents = defaultdict(lambda : None)

    dist[start] = 0

    heap : list[tuple[int, Hanoi]] = [(0, start)]
    explored = 0

    while heap:
        current_cost, node = heapq.heappop(heap)
        explored += 1

        if node.is_final():
            return True, current_cost, explored

        if current_cost > dist[node]:
            continue

        for neighbor in node.successors().values():
            new_cost = current_cost + 1

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parents[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return False, float('inf'), explored
