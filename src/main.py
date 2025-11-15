from analyses.graph_analyses import benchmark_graph
from utils.graph_utils import *

results = benchmark_graph(
    sizes=[10, 20, 40, 80, 160, 320],
    repeats=100,
    oriented=True,
    weight=(1, 1)
)

export_to_csv(results)
plot_metric_for_all_algos(results, "time")
plot_metric_for_all_algos(results, "memory")
plot_metric_for_all_algos(results, "explored")
