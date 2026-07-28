# Exp 3 — Clustering Univariate Gaussians, k=3

## Objective

Extends exp2 to k=3 clusters. With three Gaussian families having different
spreads, the Fisher-Rao metric captures both mean and variance separation,
demonstrating a measurable advantage over Euclidean distance.

## Parameters

| Parameter | Value |
|-----------|-------|
| k         | 3     |
| t         | 100 distributions / cluster |
| n         | 30 samples / distribution  |
| replications | 100 Monte Carlo |
| (μ₁, σ₁) | (1, 1.0) |
| (μ₂, σ₂) | (2, 1.5) |
| (μ₃, σ₃) | (3, 2.0) |

Varying σ values (1.0, 1.5, 2.0) make Fisher-Rao non-trivially different from
Euclidean distance — the metric accounts for the geometry of the Gaussian
statistical manifold, not just parameter-space proximity.

## Replicated Results (seed=42, 100 reps)

| Algorithm | R | Python |
|-----------|---|--------|
| K-Means + Fisher-Rao      | 0.978 ± 0.001 | 0.979 ± 0.001 |
| K-Means + Euclidean       | 0.965 ± 0.001 | 0.968 ± 0.001 |
| Hierarchical + Fisher-Rao | 0.941 ± 0.005 | 0.932 ± 0.006 |
| Hierarchical + Euclidean  | 0.889 ± 0.012 | 0.901 ± 0.010 |

Fisher-Rao > Euclidean in all four conditions. Win rates (R): K-Means 85/100,
Hierarchical 58/100.

## Files

- `R/data_generation.R` — Zhang Ch.7 pipeline (same as exp2)
- `R/clustering_k3.R`   — clustering functions with k=3 label-matching
- `python/data_generation.py` — mirrors R implementation
- `python/clustering_k3.py`   — mirrors R implementation
- `notebooks/exp3_clustering_k3.Rmd` — entry point, renders accuracy table
- `results/tables/` — CSV outputs from notebook run
