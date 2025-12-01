from analyses.graph_analyses import benchmark_graph
from analyses.grid_analyses import benchmark_grid
from analyses.hanoi_analyses import benchmark_hanoi
from analyses.canibmissio_analyse import benchmark_canibmissio
from utils.graph_utils import plot_metric_for_all_algos, export_to_csv
from utils.grid_utils import plot_metric_for_all_algos as plot_metric_grid, export_to_csv as export_to_csv_grid
from utils.hanoi_utils import plot_metric_for_all_algos as plot_metric_hanoi, export_to_csv as export_to_csv_hanoi
from utils.canibmissio_utils import plot_metric_for_all_algos as plot_metric_canibmissio, export_to_csv as export_to_csv_canibmissio

results = benchmark_graph(
    sizes=[10, 20, 40, 80, 160, 320],
    repeats=100,
    oriented=True,
    weight=(1, 1)
)

export_to_csv(results)
metrics = ["time", "memory", "explored"]
algos = ['BFS', 'DFS', 'Dijkstra']
for metric in metrics:
    plot_metric_for_all_algos(results, algos, metric, f'./figures/{metric}_graph.png')

results = benchmark_hanoi(
    sizes=[2, 3,4, 5, 6, 7, 8],
    repeats=20
)

export_to_csv_hanoi(results)
metrics = ["time", "memory", "explored"]
algos = ['BFS', 'DFS', 'Dijkstra', 'A*', 'IDA*', 'IDA* (bad h())']
# algos = ['BFS', 'DFS', 'Dijkstra', 'A*', 'IDA*']
# algos = ['BFS', 'DFS', 'Dijkstra', 'A*']
for metric in metrics:
    plot_metric_hanoi(results, algos, metric, f'./figures/{metric}_hanoi.png')

results = benchmark_canibmissio(
    number_missio_canib=[3, 4, 5, 7, 10, 15, 20],
    repeats=20
)

export_to_csv_canibmissio(results)
metrics = ["time", "memory", "explored"]
algos = ['BFS', 'DFS', 'Dijkstra', 'A*', 'IDA*']
algos_without_ida = ['BFS', 'DFS', 'Dijkstra', 'A*']
# algos = ['BFS', 'DFS', 'Dijkstra', 'A*', 'IDA*']
# algos = ['BFS', 'DFS', 'Dijkstra', 'A*']
for metric in metrics:
    plot_metric_canibmissio(results, algos, metric, f'./figures/{metric}_canibmissio.png')
    plot_metric_canibmissio(results, algos_without_ida, metric, f'./figures/{metric}_canibmissio_no_ida.png')



# results = benchmark_grid(
#     sizes=[40, 80, 160, 320],
#     nb_walls=[0,5, 8],
#     wall_sizes=[(0,2),(1,5),(5,5)],
#     repeats=10,
# )

# algos.extend(["A*", "IDA*"])
# export_to_csv_grid(results)
# for metric in metrics:
#     plot_metric_grid(results, algos, metric, f'./figures/{metric}_grid.png')
