# Maximum Cut Project

This repository provides a research codebase for experimenting with algorithms on the Maximum Cut problem in weighted undirected graphs. Four algorithms are included:

1. **Exact Brute-force** – Exhaustive enumeration of all possible cuts.
2. **Exact Solver-based** – Formulates the problem as an integer program and solves it with a solver such as Gurobi (or any solver available through `cvxpy`).
3. **Goemans–Williamson** – A randomized rounding approximation algorithm based on semidefinite programming.
4. **QAOA** – A quantum-inspired approach implemented using a simulator (e.g. Cirq or PennyLane).

The goal is to compare performance and solution quality across these methods on graphs of varying size and density.

## Installation

Create a virtual environment and install the dependencies from `requirements.txt`:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note: Installing commercial solvers such as Gurobi requires a valid license. The code can also fall back to open-source solvers available via `cvxpy`.

## Data

Graph instances can be generated with `src/data.py`:

```bash
python src/data.py --generate --n 100 --type random
```

This creates a random graph and prints basic statistics. Custom graphs can be loaded from edge list files as well.

## Running experiments

```bash
python experiments/run_experiments.py --config experiments/config.yaml
```

The script loads the configuration, runs all algorithms on the specified graph instances, and stores raw results in `results/`.

## Testing

```bash
pytest tests/
```

## Analysis

Open the Jupyter notebook for analysis and visualization:

```bash
jupyter notebook notebooks/analysis.ipynb
```

The notebook loads the results, computes statistics, and reproduces all plots. Cells performing the Wilcoxon signed-rank tests and Friedman tests are highlighted in the notebook so their outputs can be interpreted directly.

