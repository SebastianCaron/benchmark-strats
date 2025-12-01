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

def bfs_explored(graph, cm, *args, **kwargs):
    return graph.BFS(cm, *args, **kwargs)[1]

def dfs_explored(graph, cm, *args, **kwargs):
    return graph.DFS(cm, *args, **kwargs)[1]

def dijkstra_explored(graph, cm, *args, **kwargs):
    return graph.DIJKSTRA(cm, *args, **kwargs)[1]

def astar_explored(graph, cm, *args, **kwargs):
    return graph.ASTAR(cm, *args, **kwargs)[1]

def idastar_explored(graph, cm, *args, **kwargs):
    return graph.IDASTAR(cm, *args, **kwargs)[1]

def benchmark_canibmissio(
    number_missio_canib=[10,20,40,80],
    max_node = [20,40,80,160],
    repeats=50,
    results = []
):
    for nb_can_mis, m_node in zip(number_missio_canib, max_node):
        alg_results = {
            key : {"time": [], "memory": [], "explored": []} 
            for key in ["BFS", "DFS", "Dijkstra", "A*", "IDA*"]
        }
        const = CONST(nb_can_mis, nb_can_mis, 2, m_node)
        for _ in range(repeats):
            graph = Graph()
            cm = State(nb_can_mis, nb_can_mis, Direction.OLD_TO_NEW, 0, 0, 0, const)

            t, m, e = measure(bfs_explored, graph, cm)
            alg_results["BFS"]["time"].append(t)
            alg_results["BFS"]["memory"].append(m)
            alg_results["BFS"]["explored"].append(e)
            
            t, m, e = measure(dfs_explored, graph, cm)
            alg_results["DFS"]["time"].append(t)
            alg_results["DFS"]["memory"].append(m)
            alg_results["DFS"]["explored"].append(e)
            
            t, m, e = measure(dijkstra_explored, graph, cm)
            alg_results["Dijkstra"]["time"].append(t)
            alg_results["Dijkstra"]["memory"].append(m)
            alg_results["Dijkstra"]["explored"].append(e)

             
            t, m, e = measure(astar_explored, graph, cm)
            alg_results["A*"]["time"].append(t)
            alg_results["A*"]["memory"].append(m)
            alg_results["A*"]["explored"].append(e)

            t, m, e = measure(idastar_explored, graph, cm)
            alg_results["IDA*"]["time"].append(t)
            alg_results["IDA*"]["memory"].append(m)
            alg_results["IDA*"]["explored"].append(e)
            
        results.append((nb_can_mis, alg_results))

    return results