import matplotlib.pyplot as plt
import statistics
import csv

def plot_metric_for_all_algos(results : list, algos: list, metric : str, filename : str):
    plt.figure(figsize=(10, 6))

    for algo in algos:
        sizes = []
        means = []

        for size, algos_data in results:
            if algo in algos_data and metric in algos_data[algo]:
                values = algos_data[algo][metric]
                sizes.append(size)
                means.append(statistics.mean(values))

        if sizes:
            plt.plot(sizes, means, marker='o', label=algo)

    plt.title(f"Comparaison des algorithmes — {metric}")
    plt.xlabel("Taille de la tour")
    plt.ylabel(metric.capitalize())
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, format="png")
    plt.close()


def export_to_csv(results, filename="benchmark_hanoi.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["size", "algorithm", "metric", "mean", "std", "values"])

        for size, algos in results:
            for algo_name, metrics in algos.items():
                for metric_name, values in metrics.items():
                    mean_val = statistics.mean(values)
                    std_val = statistics.stdev(values) if len(values) > 1 else 0.0
                    writer.writerow([
                        size,
                        algo_name,
                        metric_name,
                        mean_val,
                        std_val,
                        ";".join(map(str, values))
                    ])
