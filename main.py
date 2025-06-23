from experiments import run_experiments, wilcoxon_signed_rank

if __name__ == '__main__':
    sizes = [4, 5]
    results = run_experiments(sizes, runs=1)
    for alg, data in results.items():
        avg_val = sum(d['value'] for d in data) / len(data)
        avg_time = sum(d['time'] for d in data) / len(data)
        print(f"{alg}: value={avg_val:.2f} time={avg_time:.4f}s")

    # Example Wilcoxon test between brute force and branch and bound times
    times_brute = [d['time'] for d in results['brute_force']]
    times_bb = [d['time'] for d in results['branch_and_bound']]
    z = wilcoxon_signed_rank(times_brute, times_bb)
    print(f"Wilcoxon statistic (brute_force vs branch_and_bound): {z:.3f}")
