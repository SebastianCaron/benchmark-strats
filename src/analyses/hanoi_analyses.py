from problems.hanoi import *

import time
import tracemalloc
import statistics

def measure(func, *args, **kwargs):

    tracemalloc.start()
    start_time = time.perf_counter()

    explored = func(*args, **kwargs)

    elapsed = (time.perf_counter() - start_time) * 1000  # ms
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed, peak / 1024, explored

def bfs_explored(*args, **kwargs):
    return bfs_hanoi(*args, **kwargs)[1]

def dfs_explored(*args, **kwargs):
    return dfs_hanoi(*args, **kwargs)[1]

def dijkstra_explored(*args, **kwargs):
    return dijkstra_hanoi(*args, **kwargs)[2]


def benchmark_hanoi(
    sizes=[2,3,5,10],
    repeats=50
):
    results = []

    for size in sizes:
        alg_results = {
            key : {"time": [], "memory": [], "explored": []} 
            for key in ["BFS", "DFS", "Dijkstra"]
        }

        for _ in range(repeats):
            h = Hanoi(size)

            t, m, e = measure(bfs_explored, h)
            alg_results["BFS"]["time"].append(t)
            alg_results["BFS"]["memory"].append(m)
            alg_results["BFS"]["explored"].append(e)
            
            t, m, e = measure(dfs_explored, h)
            alg_results["DFS"]["time"].append(t)
            alg_results["DFS"]["memory"].append(m)
            alg_results["DFS"]["explored"].append(e)
            
            t, m, e = measure(dijkstra_explored, h)
            alg_results["Dijkstra"]["time"].append(t)
            alg_results["Dijkstra"]["memory"].append(m)
            alg_results["Dijkstra"]["explored"].append(e)
            
            
            # print((size))
        results.append((size, alg_results))

    return results