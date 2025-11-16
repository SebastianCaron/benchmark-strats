from problems.grid import *

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
    return bfs_grid(*args, **kwargs)[1]

def dfs_explored(*args, **kwargs):
    return dfs_grid(*args, **kwargs)[1]

def dijkstra_explored(*args, **kwargs):
    return dijkstra_grid(*args, **kwargs)[2]

def astar_explored(*args, **kwargs):
    return astar(*args, **kwargs)[2]

def idastar_explored(*args, **kwargs):
    return ida_star(*args, **kwargs)[2]

def benchmark_grid(
    sizes=[10, 20, 40, 80],
    nb_walls=[0,5, 8],
    wall_sizes=[(0,2),(1,5),(5,5)],
    repeats=50
):
    results = []

    for size in sizes:
        for nb_wall in nb_walls:
            for wall_size in wall_sizes:

                alg_results = {
                    key : {"time": [], "memory": [], "explored": []} 
                    for key in ["BFS", "DFS", "Dijkstra", "A*", "IDA*"]
                }

                for _ in range(repeats):
                    g = Grid(size=size, nb_walls=nb_wall, wall_size=wall_size)

                    t, m, e = measure(bfs_explored, g)
                    alg_results["BFS"]["time"].append(t)
                    alg_results["BFS"]["memory"].append(m)
                    alg_results["BFS"]["explored"].append(e)
                    
                    t, m, e = measure(dfs_explored, g)
                    alg_results["DFS"]["time"].append(t)
                    alg_results["DFS"]["memory"].append(m)
                    alg_results["DFS"]["explored"].append(e)
                    
                    t, m, e = measure(dijkstra_explored, g)
                    alg_results["Dijkstra"]["time"].append(t)
                    alg_results["Dijkstra"]["memory"].append(m)
                    alg_results["Dijkstra"]["explored"].append(e)
                    
                    t, m, e = measure(astar_explored, g)
                    alg_results["A*"]["time"].append(t)
                    alg_results["A*"]["memory"].append(m)
                    alg_results["A*"]["explored"].append(e)

                    t, m, e = measure(idastar_explored, g)
                    alg_results["IDA*"]["time"].append(t)
                    alg_results["IDA*"]["memory"].append(m)
                    alg_results["IDA*"]["explored"].append(e)
                    
                    print((size, nb_wall, wall_size))
        results.append((size, nb_wall, wall_size, alg_results))

    return results