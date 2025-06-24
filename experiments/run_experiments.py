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
    "gw_trials": [5],
    "qaoa_depths": [1],
    "qaoa_steps": [50],
    "qaoa_repeats": 5,
}

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    alg = cfg.setdefault("algorithms", {})
    alg.setdefault("gw_trials", defaults["gw_trials"])
    alg.setdefault("qaoa_depths", defaults["qaoa_depths"])
    alg.setdefault("qaoa_steps", defaults["qaoa_steps"])
    alg.setdefault("qaoa_repeats", defaults["qaoa_repeats"])
    return cfg

def run(config_path: str) -> None:
    cfg = load_config(config_path)
    results: list[dict] = []
    for spec in cfg["graphs"]:
        g = generate_random_graph(
            spec["n"],
            spec.get("p", 0.5),
            tuple(spec.get("weight_range", [1, 10])),
        )
        label = f"n{spec['n']}_p{spec.get('p',0.5)}"

        t0 = time.perf_counter()
        _, val = maxcut_bruteforce(g)
        results.append({
            "alg": "bruteforce",
            "graph": label,
            "value": val,
            "time": time.perf_counter() - t0,
        })

        t0 = time.perf_counter()
        _, val = maxcut_solver(g)
        results.append({
            "alg": "solver",
            "graph": label,
            "value": val,
            "time": time.perf_counter() - t0,
        })

        for trials in cfg["algorithms"]["gw_trials"]:
            t0 = time.perf_counter()
            _, val = maxcut_goemans_williamson(g, trials=trials)
            results.append({
                "alg": f"gw_t{trials}",
                "graph": label,
                "value": val,
                "time": time.perf_counter() - t0,
            })

        steps = cfg["algorithms"]["qaoa_steps"][0]
        for p in cfg["algorithms"]["qaoa_depths"]:
            for r in range(cfg["algorithms"]["qaoa_repeats"]):
                t0 = time.perf_counter()
                _, val = maxcut_qaoa(g, p=p, steps=steps)
                results.append({
                    "alg": f"qaoa_p{p}_r{r}",
                    "graph": label,
                    "value": val,
                    "time": time.perf_counter() - t0,
                })

    df = pd.DataFrame(results)
    Path("results").mkdir(exist_ok=True)
    out_path = Path("results") / "results.jsonl"
    df.to_json(out_path, orient="records", lines=True)
    print(f"Saved results to {out_path}")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="experiments/config.yaml")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run(args.config)
