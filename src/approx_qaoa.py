from __future__ import annotations
from typing import Tuple, List

import networkx as nx
import numpy as np
import pennylane as qml

def maxcut_qaoa(g: nx.Graph, p: int = 1, steps: int = 50) -> Tuple[List[int], float]:
    n = g.number_of_nodes()
    edges = [(i, j, data.get("weight", 1.0)) for i, j, data in g.edges(data=True)]
    dev = qml.device("default.qubit", wires=n, shots=1)

    @qml.qnode(dev)
    def circuit(gammas, betas):
        for i in range(n):
            qml.Hadamard(wires=i)
        for layer in range(p):
            gamma = gammas[layer]
            for i, j, w in edges:
                qml.CNOT(wires=[i, j])
                qml.RZ(-gamma * w, wires=j)
                qml.CNOT(wires=[i, j])
            beta = betas[layer]
            for i in range(n):
                qml.RX(2 * beta, wires=i)
        return qml.sample(wires=list(range(n)))

    gammas = np.random.uniform(0, np.pi, size=p)
    betas = np.random.uniform(0, np.pi, size=p)
    bitstr = list(circuit(gammas, betas))
    cut = [i for i, bit in enumerate(bitstr) if bit == 1]
    value = sum(w for i, j, w in edges if bitstr[i] != bitstr[j])
    return cut, float(value)
