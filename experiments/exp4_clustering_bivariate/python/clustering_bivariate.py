# ============================================================
# File: python/clustering_bivariate.py
# Experiment: exp4_clustering_bivariate
# Description: K-Means and hierarchical clustering with bivariate Fisher-Rao / Euclidean
# Reference: Zhang (2017) Ch.8, Sec.8.3; Selim & Ismail (1984)
# ============================================================

import os
import sys
from itertools import permutations

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../exp1_distances/python"))

from data_generation_bivariate import generate_dataset_bivariate  # noqa: E402


# --- Vectorized bivariate Fisher-Rao (inlined for performance) ---------------

def _fr_bivariate_pair_arrays(
    mu_i: np.ndarray, s1_i: np.ndarray, s2_i: np.ndarray,
    mu_j: np.ndarray, s1_j: np.ndarray, s2_j: np.ndarray,
) -> np.ndarray:
    """Bivariate Fisher-Rao distance for arrays of parameter pairs. Zhang eq. 4.12/8.2."""
    dm = (mu_i - mu_j) / np.sqrt(2)

    A1 = np.sqrt(dm**2 + (s1_i + s1_j)**2)
    B1 = np.sqrt(dm**2 + (s1_i - s1_j)**2)
    t1 = np.log((A1 + B1)**2 / (4 * s1_i * s1_j))

    A2 = np.sqrt(dm**2 + (s2_i + s2_j)**2)
    B2 = np.sqrt(dm**2 + (s2_i - s2_j)**2)
    t2 = np.log((A2 + B2)**2 / (4 * s2_i * s2_j))

    return np.sqrt(2 * (t1**2 + t2**2))


def fisher_rao_bivariate_dist_matrix(params: dict[str, np.ndarray]) -> np.ndarray:
    """Pairwise bivariate Fisher-Rao distance matrix (vectorised over upper triangle)."""
    mu = params["mu_hat"]
    s1 = params["sigma1_hat"]
    s2 = params["sigma2_hat"]
    n  = len(mu)
    rows, cols = np.triu_indices(n, k=1)
    d   = _fr_bivariate_pair_arrays(mu[rows], s1[rows], s2[rows],
                                     mu[cols], s1[cols], s2[cols])
    mat = np.zeros((n, n))
    mat[rows, cols] = d
    mat[cols, rows] = d
    return mat


def _fr_bivariate_to_center(
    mu: np.ndarray, s1: np.ndarray, s2: np.ndarray,
    mu_c: float, s1_c: float, s2_c: float,
) -> np.ndarray:
    """Distances from all n points to one center."""
    return _fr_bivariate_pair_arrays(
        mu, s1, s2,
        np.full_like(mu, mu_c), np.full_like(s1, s1_c), np.full_like(s2, s2_c),
    )


def euclidean_dist_matrix_3d(params: dict[str, np.ndarray]) -> np.ndarray:
    """Pairwise Euclidean distance matrix in (mu, sigma1, sigma2) space."""
    pts = np.column_stack([params["mu_hat"], params["sigma1_hat"], params["sigma2_hat"]])
    return squareform(pdist(pts, metric="euclidean"))


# --- K-Means with bivariate Fisher-Rao ---------------------------------------

def kmeans_fr_bivariate(
    params: dict[str, np.ndarray],
    k: int,
    max_iter: int = 100,
    n_init: int = 10,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """K-Means using bivariate Fisher-Rao distance for assignment.

    Centroid update: arithmetic mean of (mu_hat, sigma1_hat, sigma2_hat).
    Best of n_init random restarts. Zhang (2017) Ch.8; Selim (1984).
    Returns 1-indexed integer array of cluster labels.
    """
    if rng is None:
        rng = np.random.default_rng()
    mu = params["mu_hat"]
    s1 = params["sigma1_hat"]
    s2 = params["sigma2_hat"]
    n  = len(mu)

    best_labels  = np.zeros(n, dtype=int)
    best_inertia = np.inf

    for _ in range(n_init):
        init_idx = rng.choice(n, size=k, replace=False)
        cmu = mu[init_idx].copy()
        cs1 = s1[init_idx].copy()
        cs2 = s2[init_idx].copy()
        labels = np.zeros(n, dtype=int)
        dists  = np.empty((n, k))

        for _ in range(max_iter):
            for cl in range(k):
                dists[:, cl] = _fr_bivariate_to_center(mu, s1, s2, cmu[cl], cs1[cl], cs2[cl])
            new_labels = np.argmin(dists, axis=1)

            if np.array_equal(new_labels, labels):
                labels = new_labels
                break
            labels = new_labels

            for cl in range(k):
                mask = labels == cl
                if mask.any():
                    cmu[cl] = mu[mask].mean()
                    cs1[cl] = s1[mask].mean()
                    cs2[cl] = s2[mask].mean()

        inertia = np.sum(dists[np.arange(n), labels] ** 2)
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels  = labels + 1      # 1-indexed

    return best_labels


# --- Hierarchical clustering -------------------------------------------------

def hclust_custom(
    dist_matrix: np.ndarray, k: int, method: str = "complete"
) -> np.ndarray:
    """Hierarchical clustering from a precomputed distance matrix. Returns 1-indexed labels."""
    condensed = squareform(dist_matrix)
    Z         = linkage(condensed, method=method)
    return fcluster(Z, t=k, criterion="maxclust")


# --- Accuracy with optimal label matching (k=3: all 3! permutations) ---------

def match_accuracy_k3(true_labels: np.ndarray, pred_labels: np.ndarray) -> float:
    """Best accuracy over all 3! = 6 label permutations. Zhang (2017) Ch.8."""
    classes = np.unique(pred_labels)
    best = 0.0
    for perm in permutations(classes):
        mapping = dict(zip(classes, perm))
        mapped  = np.vectorize(mapping.get)(pred_labels)
        acc     = float(np.mean(mapped == true_labels))
        if acc > best:
            best = acc
    return best


# --- Monte Carlo replication driver ------------------------------------------

def run_replications(
    mu_list: list[float],
    sigma_list: list[list[float]],
    k: int = 3,
    t: int = 100,
    n: int = 30,
    n_rep: int = 100,
    hclust_method: str = "complete",
    seed: int = 42,
) -> dict[str, np.ndarray]:
    """Run n_rep Monte Carlo replications; return dict of accuracy arrays."""
    rng   = np.random.default_rng(seed)
    km_fr = np.empty(n_rep)
    km_eu = np.empty(n_rep)
    hc_fr = np.empty(n_rep)
    hc_eu = np.empty(n_rep)

    from sklearn.cluster import KMeans  # noqa: PLC0415

    for r in range(n_rep):
        dat         = generate_dataset_bivariate(mu_list, sigma_list, t=t, n=n, rng=rng)
        true_labels = dat["cluster"]
        pts         = np.column_stack([dat["mu_hat"], dat["sigma1_hat"], dat["sigma2_hat"]])

        fr_dist = fisher_rao_bivariate_dist_matrix(dat)
        eu_dist = euclidean_dist_matrix_3d(dat)

        km_fr_pred = kmeans_fr_bivariate(dat, k=k, rng=rng)
        eu_km_pred = KMeans(n_clusters=k, n_init=10,
                            random_state=int(rng.integers(1_000_000))).fit_predict(pts) + 1

        km_fr[r] = match_accuracy_k3(true_labels, km_fr_pred)
        km_eu[r] = match_accuracy_k3(true_labels, eu_km_pred)
        hc_fr[r] = match_accuracy_k3(true_labels, hclust_custom(fr_dist, k=k, method=hclust_method))
        hc_eu[r] = match_accuracy_k3(true_labels, hclust_custom(eu_dist, k=k, method=hclust_method))

    return {"km_fr": km_fr, "km_eu": km_eu, "hc_fr": hc_fr, "hc_eu": hc_eu}


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    mu_list    = [1.0,  1.5,  2.0]
    sigma_list = [[1.0, 2.0], [1.5, 2.5], [2.0, 3.0]]

    print("Running 100 Monte Carlo replications (k=3, t=100, n=30, bivariate)…")
    results = run_replications(mu_list, sigma_list)
    n_rep   = 100

    zhang_ref = {
        "K-Means + Fisher-Rao":      "0.937 ± 0.001",
        "K-Means + Euclidean":        "0.877 ± 0.003",
        "Hierarchical + Fisher-Rao":  "0.860 ± 0.008",
        "Hierarchical + Euclidean":   "0.716 ± 0.012",
    }

    print(f"\n{'Algorithm':<30}  {'Replicated':>15}  {'Zhang (2017)':>15}")
    print("-" * 65)
    labels_map = {
        "K-Means + Fisher-Rao":      "km_fr",
        "K-Means + Euclidean":        "km_eu",
        "Hierarchical + Fisher-Rao":  "hc_fr",
        "Hierarchical + Euclidean":   "hc_eu",
    }
    for algo, col in labels_map.items():
        arr   = results[col]
        rep   = f"{arr.mean():.3f} ± {arr.std() / n_rep**0.5:.3f}"
        zhang = zhang_ref[algo]
        print(f"{algo:<30}  {rep:>15}  {zhang:>15}")
