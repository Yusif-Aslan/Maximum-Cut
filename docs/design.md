# Design Overview

This document outlines the structure of the Maximum Cut project and summarizes the algorithms implemented.

## Algorithms

- **Exact Brute-force**: Enumerates all possible 2^n cuts and selects the one with the maximum weight.
- **Exact Solver-based**: Formulates the cut problem as a binary quadratic program solved with an external solver via `cvxpy`.
- **Goemans–Williamson**: Solves the SDP relaxation and rounds via randomized hyperplane cuts.
- **QAOA**: Implements a quantum approximate optimization algorithm using a simulator backend.

## Experiments

`experiments/run_experiments.py` provides a command line interface that loads graphs (generated or from files), runs all algorithms, and saves results in CSV format under `results/`.

The configuration for experiment sweeps is stored in `experiments/config.yaml`. Parameters include graph sizes, densities, and algorithm-specific hyperparameters.

## Testing

Basic unit tests validate the data loader and that each algorithm returns a cut and a value. Integration tests run the full experiment pipeline on a tiny graph to ensure end-to-end functionality.

