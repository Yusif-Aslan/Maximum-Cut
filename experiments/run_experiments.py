from __future__ import annotations
import argparse
import time
from pathlib import Path

import yaml
import pandas as pd

from src import (
    generate_random_graph,
    maxcut_bruteforce,
    maxcut_solver,
    maxcut_goemans_williamson,
    maxcut_qaoa,
)

defaults = {
    "exact_repeats": 5,
    "gw_trials":     [5, 10, 20],
    "gw_repeats":    10,
    "qaoa_depths":   [1, 2],
    "qaoa_steps":    [50],
    "qaoa_repeats":  10,
}

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    alg = cfg.setdefault("algorithms", {})
    alg.setdefault("exact_repeats", defaults["exact_repeats"])
    alg.setdefault("gw_trials",     defaults["gw_trials"])
    alg.setdefault("gw_repeats",    defaults["gw_repeats"])
    alg.setdefault("qaoa_depths",   defaults["qaoa_depths"])
    alg.setdefault("qaoa_steps",    defaults["qaoa_steps"])
    alg.setdefault("qaoa_repeats",  defaults["qaoa_repeats"])
    return cfg

def run(config_path: str) -> None:
    cfg     = load_config(config_path)
    results = []

    for spec in cfg["graphs"]:
        g     = generate_random_graph(
                    spec["n"],
                    spec.get("p", 0.5),
                    tuple(spec.get("weight_range", [1, 10])),
                )
        label = f"n{spec['n']}_p{spec.get('p',0.5)}"

        # exact algorithms repeated
        for _ in range(cfg["algorithms"]["exact_repeats"]):
            t0 = time.perf_counter()
            _, v = maxcut_bruteforce(g)
            results.append({"alg":"bruteforce","graph":label,"value":v,"time":time.perf_counter()-t0})
            t0 = time.perf_counter()
            _, v = maxcut_solver(g)
            results.append({"alg":"solver","graph":label,"value":v,"time":time.perf_counter()-t0})

        # Goemans–Williamson with repeats
        for trials in cfg["algorithms"]["gw_trials"]:
            for r in range(cfg["algorithms"]["gw_repeats"]):
                t0 = time.perf_counter()
                _, v = maxcut_goemans_williamson(g, trials=trials)
                results.append({
                    "alg":  f"gw_t{trials}_r{r}",
                    "graph":label,
                    "value":v,
                    "time": time.perf_counter()-t0,
                })

        # QAOA with repeats
        steps = cfg["algorithms"]["qaoa_steps"][0]
        for p in cfg["algorithms"]["qaoa_depths"]:
            for r in range(cfg["algorithms"]["qaoa_repeats"]):
                t0 = time.perf_counter()
                _, v = maxcut_qaoa(g, p=p, steps=steps)
                results.append({
                    "alg":  f"qaoa_p{p}_r{r}",
                    "graph":label,
                    "value":v,
                    "time": time.perf_counter()-t0,
                })

    df = pd.DataFrame(results)
    Path("results").mkdir(exist_ok=True)
    df.to_json(Path("results")/"results.jsonl", orient="records", lines=True)
    print("Saved results to results/results.jsonl")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="experiments/config.yaml")
    return p.parse_args()

if __name__ == "__main__":
    run(parse_args().config)
