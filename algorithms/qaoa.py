import cmath
import math
import itertools


def _apply_cost_operator(state, graph, gamma):
    new_state = state.copy()
    for idx in range(len(state)):
        # bitstring representation
        phase = 0.0
        for u, v, w in graph.all_edges():
            bit_u = (idx >> u) & 1
            bit_v = (idx >> v) & 1
            if bit_u != bit_v:
                phase += w
        new_state[idx] *= cmath.exp(-1j * gamma * phase)
    return new_state


def _apply_mixer_operator(state, beta, n):
    new_state = [0j] * len(state)
    for idx in range(len(state)):
        amplitude = state[idx]
        for qubit in range(n):
            if (idx >> qubit) & 1:
                flipped = idx & ~(1 << qubit)
            else:
                flipped = idx | (1 << qubit)
            new_state[flipped] += amplitude * (-1j * math.sin(beta)) / n
        new_state[idx] += amplitude * math.cos(beta)
    return new_state


def _expectation(state, graph):
    value = 0.0
    for idx, amp in enumerate(state):
        prob = abs(amp) ** 2
        cost = 0
        for u, v, w in graph.all_edges():
            if ((idx >> u) & 1) != ((idx >> v) & 1):
                cost += w
        value += prob * cost
    return value


def qaoa_max_cut(graph, steps=5):
    n = graph.num_vertices
    best_val = -1
    best_angles = (0, 0)
    for gamma_step in range(steps):
        gamma = math.pi * gamma_step / steps
        for beta_step in range(steps):
            beta = math.pi * beta_step / steps
            # start in uniform superposition
            size = 1 << n
            state = [1 / math.sqrt(size)] * size
            state = _apply_cost_operator(state, graph, gamma)
            state = _apply_mixer_operator(state, beta, n)
            val = _expectation(state, graph)
            if val > best_val:
                best_val = val
                best_angles = (gamma, beta)
    # simple deterministic rounding: use expectation of Z for each qubit
    gamma, beta = best_angles
    size = 1 << n
    state = [1 / math.sqrt(size)] * size
    state = _apply_cost_operator(state, graph, gamma)
    state = _apply_mixer_operator(state, beta, n)
    bits = []
    for qubit in range(n):
        prob1 = 0.0
        for idx, amp in enumerate(state):
            if (idx >> qubit) & 1:
                prob1 += abs(amp) ** 2
        bits.append(1 if prob1 >= 0.5 else 0)
    return best_val, bits
