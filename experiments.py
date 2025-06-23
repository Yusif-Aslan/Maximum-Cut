import random
import time
import math
from statistics import mean, stdev

from graphs import Graph
from algorithms import brute_force, branch_and_bound, goemans_williamson, qaoa, ilp_solver


def generate_random_graph(n, p=0.5, weight_range=(1, 1)):
    g = Graph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < p:
                w = random.randint(weight_range[0], weight_range[1])
                g.add_edge(u, v, w)
    return g


def measure_algorithm(func, graph):
    start = time.time()
    value, bits = func(graph)
    duration = time.time() - start
    return value, duration


def run_experiments(num_vertices_list, runs=3):
    algs = {
        'brute_force': brute_force.max_cut_brute_force,
        'branch_and_bound': branch_and_bound.max_cut_branch_and_bound,
        'ilp_solver': ilp_solver.max_cut_ilp,
        'goemans_williamson': goemans_williamson.goemans_williamson,
        'qaoa': qaoa.qaoa_max_cut,
    }
    results = {name: [] for name in algs}
    for n in num_vertices_list:
        for _ in range(runs):
            g = generate_random_graph(n)
            opt_value, _ = brute_force.max_cut_brute_force(g)
            for name, func in algs.items():
                value, duration = measure_algorithm(func, g)
                gap = 0 if opt_value == 0 else (opt_value - value) / opt_value
                results[name].append({'n': n, 'value': value, 'time': duration, 'gap': gap})
    return results


def summarize_results(results):
    """Compute mean and standard deviation of metrics for each algorithm."""
    summary = {}
    for name, records in results.items():
        times = [r['time'] for r in records]
        values = [r['value'] for r in records]
        gaps = [r['gap'] for r in records]
        summary[name] = {
            'time_mean': mean(times),
            'time_sd': stdev(times) if len(times) > 1 else 0.0,
            'value_mean': mean(values),
            'value_sd': stdev(values) if len(values) > 1 else 0.0,
            'gap_mean': mean(gaps),
        }
    return summary


def pairwise_wilcoxon(results, key='time'):
    """Return Wilcoxon statistics for each algorithm pair."""
    algs = list(results.keys())
    matrix = {}
    for i, a in enumerate(algs):
        for j, b in enumerate(algs):
            if i >= j:
                continue
            x = [r[key] for r in results[a]]
            y = [r[key] for r in results[b]]
            matrix[(a, b)] = wilcoxon_signed_rank(x, y)
    return matrix


def wilcoxon_signed_rank(data1, data2):
    """Simple Wilcoxon signed-rank test implementation."""
    diffs = [x - y for x, y in zip(data1, data2) if x != y]
    if not diffs:
        return 0.0
    ranks = [(abs(d), i) for i, d in enumerate(diffs)]
    ranks.sort()
    rank_sum_pos = 0
    rank = 1
    for abs_diff, idx in ranks:
        if diffs[idx] > 0:
            rank_sum_pos += rank
        rank += 1
    n = len(diffs)
    expected = n * (n + 1) / 4
    variance = n * (n + 1) * (2 * n + 1) / 24
    z = (rank_sum_pos - expected) / math.sqrt(variance)
    return z

