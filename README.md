# Maximum Cut Algorithms and Experiments

This repository contains simple Python implementations of algorithms for the Maximum Cut problem. Five algorithms are provided:

* `max_cut_brute_force` – exhaustive search over all partitions.
* `max_cut_branch_and_bound` – branch-and-bound search (exact).
* `goemans_williamson` – simplified version of the Goemans–Williamson approximation using random hyperplanes.
* `qaoa_max_cut` – basic QAOA simulation for Max-Cut using pure Python state vectors.
* `max_cut_ilp` – formulates an MILP solved with `pulp` (falls back to brute force if `pulp` is unavailable).

`experiments.py` includes utilities to generate random graphs, run the algorithms and collect metrics such as runtime, value and optimality gap. Helper functions compute summary statistics and perform Wilcoxon signed‑rank tests for every pair of algorithms.

Run a quick experiment using:

```bash
python3 main.py
```

All implementations work with the Python standard library. The ILP solver additionally tries to import `pulp` if available but will fall back to brute force otherwise.

## Plotting results

If `matplotlib` is installed, running `python3 main.py` will also produce a
`results.png` file containing a log--log plot of runtime versus graph size for
each algorithm. The plot uses different colors for each line and includes a
legend describing which algorithm each color corresponds to.

Graphs for the experiments are generated on-the-fly using `experiments.generate_random_graph`.
