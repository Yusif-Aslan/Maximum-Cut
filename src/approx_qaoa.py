"""Quantum Approximate Optimization Algorithm for Max-Cut using PennyLane."""

from __future__ import annotations
from typing import Tuple, List

import networkx as nx
import numpy as np
import pennylane as qml


def maxcut_qaoa(
    g: nx.Graph,
    p: int = 1,
    steps: int = 50,
) -> Tuple[List[int], float]:
    """
    Approximate max-cut using a p-layer QAOA circuit on a PennyLane simulator.

    Args:
        g: networkx Graph with edge attribute "weight".
        p: number of QAOA layers.
        steps: (ignored in this stub) number of classical optimization steps.

    Returns:
        cut: list of node indices on one side of the cut.
        value: total weight of edges crossing the cut.
    """
    n = g.number_of_nodes()
    # Collect edges as (i, j, weight)
    edges = [(i, j, data.get("weight", 1.0)) for i, j, data in g.edges(data=True)]

    # Use a shot‐based device so that calling the QNode returns a bitstring
    dev = qml.device("default.qubit", wires=n, shots=1)

    @qml.qnode(dev)
    def circuit(gammas, betas):
        # 1) Prepare uniform superposition
        for i in range(n):
            qml.Hadamard(wires=i)

        # 2) p layers of cost and mixer unitaries
        for layer in range(p):
            gamma = gammas[layer]
            # cost operator: for each edge, phase based on its weight
            for i, j, w in edges:
                qml.CNOT(wires=[i, j])
                qml.RZ(-gamma * w, wires=j)
                qml.CNOT(wires=[i, j])
            # mixer operator
            beta = betas[layer]
            for i in range(n):
                qml.RX(2 * beta, wires=i)

        # 3) Return one sample of all wires as a bitstring
        return qml.sample(wires=list(range(n)))

    # Initialize parameters (you can replace with a real optimizer loop if desired)
    gammas = np.random.uniform(0, np.pi, size=p)
    betas = np.random.uniform(0, np.pi, size=p)

    # If you want to optimize, you could do something like:
    #   opt = qml.NelderMeadOptimizer()
    #   for _ in range(steps):
    #       gammas, betas = opt.step(lambda g, b: -expected_cut_value(g, b), gammas, betas)
    # but here we'll skip the optimization and just sample once.

    # Call the QNode – it returns a length-n array of 0/1 samples
    bitstr = list(circuit(gammas, betas))

    # Build the cut and compute its weight
    cut = [i for i, bit in enumerate(bitstr) if bit == 1]
    value = sum(w for i, j, w in edges if bitstr[i] != bitstr[j])

    return cut, float(value)
