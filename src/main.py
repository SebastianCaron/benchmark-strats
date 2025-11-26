from analyses.graph_analyses import benchmark_graph
from analyses.grid_analyses import benchmark_grid
from analyses.hanoi_analyses import benchmark_hanoi
from utils.graph_utils import plot_metric_for_all_algos, export_to_csv
from utils.grid_utils import plot_metric_for_all_algos as plot_metric_grid, export_to_csv as export_to_csv_grid
from utils.hanoi_utils import plot_metric_for_all_algos as plot_metric_hanoi, export_to_csv as export_to_csv_hanoi

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
    sizes=[2, 3, 5, 7],
    repeats=100
)

export_to_csv_hanoi(results)
metrics = ["time", "memory", "explored"]
algos = ['BFS', 'DFS', 'Dijkstra']
for metric in metrics:
    plot_metric_hanoi(results, algos, metric, f'./figures/{metric}_hanoi.png')

results = benchmark_grid(
    sizes=[40, 80, 160, 320],
    nb_walls=[0,5, 8],
    wall_sizes=[(0,2),(1,5),(5,5)],
    repeats=10,
)

algos.extend(["A*", "IDA*"])
export_to_csv_grid(results)
for metric in metrics:
    plot_metric_grid(results, algos, metric, f'./figures/{metric}_grid.png')
