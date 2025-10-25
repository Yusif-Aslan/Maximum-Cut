#!/usr/bin/env python3
import argparse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, friedmanchisquare

def load_results(path, lines):
    return pd.read_json(path, orient="records", lines=lines)

def compute_gaps(df):
    opt = df[df.alg.str.startswith("solver")][["graph","value"]].set_index("graph")
    df = df.join(opt, on="graph", rsuffix="_opt")
    df["gap"] = (df["value_opt"] - df["value"]) / df["value_opt"]
    return df

def plot_cut_values(df, outfile):
    df["alg2"] = df.alg.replace(r"_r\d+$","",regex=True)
    summary = df.groupby(["graph","alg2"]).value.agg(["mean","std"]).reset_index()
    graphs = summary.graph.unique()
    algs = summary.alg2.unique()
    x = np.arange(len(graphs))
    width = 0.8/len(algs)
    fig, ax = plt.subplots()
    for i,a in enumerate(algs):
        grp = summary[summary.alg2==a].set_index("graph")
        means = [grp.loc[g,"mean"] for g in graphs]
        stds  = [grp.loc[g,"std"]  for g in graphs]
        ax.bar(x + i*width - (len(algs)-1)*width/2,
               means, width, yerr=stds, capsize=4, label=a)
    ax.set_xticks(x)
    ax.set_xticklabels(graphs)
    ax.set_ylabel("Cut value")
    ax.set_title("Comparison of all algorithms")
    ax.legend()
    plt.tight_layout()
    fig.savefig(outfile)

def plot_times(df, outfile):
    df["alg2"] = df.alg.replace(r"_r\d+$","",regex=True)
    summary = df.groupby(["graph","alg2"]).time.agg(["mean","std"]).reset_index()
    graphs = summary.graph.unique()
    algs = summary.alg2.unique()
    x = np.arange(len(graphs))
    width = 0.8/len(algs)
    fig, ax = plt.subplots()
    for i,a in enumerate(algs):
        grp = summary[summary.alg2==a].set_index("graph")
        means = [grp.loc[g,"mean"] for g in graphs]
        stds  = [grp.loc[g,"std"]  for g in graphs]
        ax.bar(x + i*width - (len(algs)-1)*width/2,
               means, width, yerr=stds, capsize=4, label=a)
    ax.set_xticks(x)
    ax.set_xticklabels(graphs)
    ax.set_yscale("log")
    ax.set_ylabel("Runtime (s, log scale)")
    ax.set_title("Runtime comparison")
    ax.legend()
    plt.tight_layout()
    fig.savefig(outfile)

def run_tests(df):
    print("Wilcoxon time: bruteforce vs solver")
    for g in df.graph.unique():
        b = df[(df.graph==g)&(df.alg=="bruteforce")].time
        s = df[(df.graph==g)&(df.alg=="solver")].time
        if len(b)>1 and len(s)>1:
            print(g, wilcoxon(b,s).pvalue)
        else:
            print(g, "skip")
    print("\nFriedman value across algorithms:")
    pivot = df.pivot_table(index="alg", columns="graph", values="value", aggfunc="mean")
    stat,p = friedmanchisquare(*[pivot.loc[a] for a in pivot.index])
    print("p-value =", p)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results", default="results/results.jsonl")
    p.add_argument("--jsonl", action="store_true")
    args = p.parse_args()

    df = load_results(args.results, args.jsonl)
    df = compute_gaps(df)

    plot_cut_values(df, "alg_comparison.png")
    plot_times(df,      "time_comparison.png")
    run_tests(df)

if __name__ == "__main__":
    main()
