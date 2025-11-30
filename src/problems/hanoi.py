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
        return (self.piles[start][-1] > self.piles[end][-1])
    
    def successors(self) -> dict[tuple[int, int], "Hanoi"]:
        res = {}
        coups = [0, 1, 2]
        for i in coups:
            for j in coups:
                if j != i and self.can_play(i, j):
                    res[(i, j)] = self.copy().play(i, j)
        return res
    
    def is_final(self):
        final_pile = 2
        for i in range(3):
            if i != final_pile and len(self.piles[i]) > 0:
                return False
        
        expected_order = list(range(1, self.size))
        return self.piles[final_pile] == expected_order

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

    def bad_heuristic(self) -> float:
        """Heuristique admissible : nombre de disques qui ne sont pas sur la pile finale (pile 2)."""
        final_pile = 2
        total_disks = sum(len(pile) for pile in self.piles)
        disks_on_final = len(self.piles[final_pile])
        return total_disks - disks_on_final
    
    def heuristic(self) -> int:
        """
        Heuristique admissible plus informative :
        On identifie le plus grand disque incorrect (k),
        puis on réduit son coût minimal en fonction de la longueur
        du préfixe correct déjà présent sur la pile finale.

        h = 2^(k - 1 - prefix)
        """
        final_pile = 2
        num_disks = self.size - 1

        final = self.piles[final_pile]

        prefix = 0
        for i in range(len(final)):
            if final[i] == i + 1:
                prefix += 1
            else:
                break
        for k in range(num_disks, 0, -1):
            if k > len(final) or final[k - 1] != k:
                exp = max(0, (k - 1) - prefix)
                return 2 ** exp

        return 0




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

def astar_hanoi(hanoi: Hanoi):
    start = hanoi

    pq = [(start.heuristic(), 0, start)]
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    visited = set()

    explored = 0

    while pq:
        f_score, g_score, node = heapq.heappop(pq)
        
        if node in visited:
            continue
            
        visited.add(node)
        explored += 1

        if node.is_final():
            return True, g_score, explored

        for neighbor in node.successors().values():
            if neighbor in visited:
                continue
                
            new_cost = g_score + 1

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                f_cost = new_cost + neighbor.heuristic()
                heapq.heappush(pq, (f_cost, new_cost, neighbor))

    return False, float('inf'), explored


def search_idastar_hanoi(hanoi: Hanoi, path, g, bound, explored, heuristic = lambda x : x.heuristic()):
    node = path[-1]
    explored[0] += 1

    f = g + heuristic(node)

    if f > bound:
        return False, f

    if node.is_final():
        return True, g

    min_bound = float('inf')

    for neighbor in node.successors().values():
        if neighbor in path:
            continue
        
        path.append(neighbor)
        found, result = search_idastar_hanoi(hanoi, path, g + 1, bound, explored, heuristic)

        if found:
            return True, result

        if result < min_bound:
            min_bound = result

        path.pop()

    return False, min_bound


def ida_star_hanoi(hanoi: Hanoi, heuristic = lambda x : x.heuristic()):
    start = hanoi

    bound = heuristic(start)
    explored = [0]

    num_disks = len(hanoi.piles[0]) if hanoi.piles[0] else 0
    max_bound = 2 ** (num_disks + 1) if num_disks > 0 else 1000

    while True:
        path = [start]
        found, result = search_idastar_hanoi(hanoi, path, 0, bound, explored, heuristic)

        if found:
            return True, result, explored[0]

        if result == float('inf'):
            return False, float('inf'), explored[0]

        bound = result
    
        if bound > max_bound:
            return False, float('inf'), explored[0]
