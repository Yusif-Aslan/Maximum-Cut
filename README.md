# Maximum Cut Algorithms and Experiments

This repository contains simple Python implementations of algorithms for the Maximum Cut problem. Four algorithms are provided:

* `max_cut_brute_force` – exhaustive search over all partitions.
* `max_cut_branch_and_bound` – branch-and-bound search (exact).
* `goemans_williamson` – simplified version of the Goemans–Williamson approximation using random hyperplanes.
* `qaoa_max_cut` – basic QAOA simulation for Max-Cut using pure Python state vectors.

`experiments.py` includes utilities to generate random graphs, run the algorithms and collect metrics such as runtime, value and optimality gap. A minimal Wilcoxon signed‑rank test is implemented to compare paired results.

Run a quick experiment using:

```bash
python3 main.py
```

The code uses only the Python standard library so no additional dependencies are required.
