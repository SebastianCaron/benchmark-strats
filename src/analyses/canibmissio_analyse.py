from problems.canib_missio import *

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
    return Graph.BFS(*args, **kwargs)[1]

def dfs_explored(*args, **kwargs):
    return Graph.DFS(*args, **kwargs)[1]

def dijkstra_explored(*args, **kwargs):
    return Graph.DIJKSTRA(*args, **kwargs)[1]

def astar_explored(*args, **kwargs):
    return Graph.ASTAR(*args, **kwargs)[1]

def idastar_explored(*args, **kwargs):
    return Graph.IDASTAR(*args, **kwargs)[1]

def benchmark_canibmissio(
    number_canib=[8,18,40,80],
    number_missio=[10,20,40,80],
    cap_boat = [2,4,6,8],
    max_node = [20,40,80,160],
    repeats=50,
    results = []
):
    for nb_can, nb_mis, cap_b, m_node in number_canib, number_missio, cap_boat, max_node:
        alg_results = {
            key : {"time": [], "memory": [], "explored": []} 
            for key in ["BFS", "DFS", "Dijkstra"]
        }
        const = CONST(nb_mis, nb_can, cap_b, m_node)
        for _ in range(repeats):

            h = State(nb_mis, nb_can, Direction.OLD_TO_NEW, 0, 0, 0, const)

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
            
        results.append((nb_mis, alg_results))

    return results