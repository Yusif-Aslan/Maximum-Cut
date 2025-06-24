"""QAOA approximation for Maximum Cut using PennyLane."""

from __future__ import annotations

from typing import Tuple, List

import networkx as nx
import numpy as np
import pennylane as qml


def maxcut_qaoa(g: nx.Graph, p: int = 1, steps: int = 50) -> Tuple[List[int], float]:
    """Quantum-inspired approximate optimization using a simulator."""
    n = g.number_of_nodes()
    dev = qml.device("default.qubit", wires=n)

    edges = [(u, v, g.edges[u, v].get("weight", 1)) for u, v in g.edges()]

    def cost_layer(gamma):
        for u, v, w in edges:
            qml.CNOT(wires=[u, v])
            qml.RZ(-gamma * w, wires=v)
            qml.CNOT(wires=[u, v])

    def mixer_layer(beta):
        for i in range(n):
            qml.RX(2 * beta, wires=i)

    @qml.qnode(dev)
    def circuit(params):
        for i in range(n):
            qml.Hadamard(wires=i)
        for t in range(p):
            cost_layer(params[0][t])
            mixer_layer(params[1][t])
        return qml.expval(qml.Hermitian(cost_matrix, wires=range(n)))

    # Build cost matrix for expectation calculation
    cost_matrix = np.zeros((2 ** n, 2 ** n))
    for u, v, w in edges:
        z = np.zeros((2 ** n, 2 ** n))
        for i in range(2 ** n):
            bit_u = (i >> u) & 1
            bit_v = (i >> v) & 1
            if bit_u != bit_v:
                z[i, i] += w
        cost_matrix += z

    params = [np.random.uniform(0, np.pi, p), np.random.uniform(0, np.pi, p)]
    opt = qml.GradientDescentOptimizer(0.1)
    for _ in range(steps):
        params = opt.step(circuit, params)
    # obtain bitstring by sampling
    sample = qml.sample(circuit, params=params, shots=1)
    sample = sample[0]
    subset = [i for i in range(n) if (sample >> i) & 1]
    value = sum(w for u, v, w in edges if ((u in subset) != (v in subset)))
    return subset, value
