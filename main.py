from experiments import (
    run_experiments,
    summarize_results,
    pairwise_wilcoxon,
    plot_results,
)

if __name__ == '__main__':
    sizes = [4, 5, 6]
    results = run_experiments(sizes, runs=1)
    summary = summarize_results(results)
    for alg, stats in summary.items():
        print(
            f"{alg}: value={stats['value_mean']:.2f}±{stats['value_sd']:.2f} "
            f"time={stats['time_mean']:.4f}s"
        )

    print("\nWilcoxon Z scores (times):")
    for (a, b), z in pairwise_wilcoxon(results).items():
        print(f"{a} vs {b}: {z:.3f}")

    plot_results(results)
