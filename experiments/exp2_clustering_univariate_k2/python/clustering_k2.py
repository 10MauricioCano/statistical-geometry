# ============================================================
# File: python/clustering_k2.py
# Experiment: exp2_clustering_univariate_k2
# Description: K-Means and hierarchical clustering with Fisher-Rao / Euclidean
# Reference: Zhang (2017) Ch.8; Selim & Ismail (1984)
# ============================================================

import os
import sys

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist, squareform

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../exp1_distances/python"))
from distances import fisher_rao_univariate  # noqa: E402

from data_generation import generate_dataset  # noqa: E402


# --- Distance matrices -------------------------------------------------------

def fisher_rao_dist_matrix(params: dict[str, np.ndarray]) -> np.ndarray:
    """Pairwise Fisher-Rao distance matrix over (mu_hat, sigma_hat) pairs."""
    mu    = params["mu_hat"]
    sigma = params["sigma_hat"]
    n     = len(mu)
    mat   = np.zeros((n, n))
    for i in range(n - 1):
        for j in range(i + 1, n):
            d          = fisher_rao_univariate(mu[i], sigma[i], mu[j], sigma[j])
            mat[i, j]  = d
            mat[j, i]  = d
    return mat


def euclidean_dist_matrix(params: dict[str, np.ndarray]) -> np.ndarray:
    """Pairwise Euclidean distance matrix over (mu_hat, sigma_hat) pairs."""
    pts = np.column_stack([params["mu_hat"], params["sigma_hat"]])
    return squareform(pdist(pts, metric="euclidean"))


# --- K-Means with Fisher-Rao distance ----------------------------------------

def kmeans_fr(
    params: dict[str, np.ndarray],
    k: int,
    max_iter: int = 100,
    n_init: int = 10,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """K-Means using Fisher-Rao distance for assignment.

    Centroid update: arithmetic mean of (mu_hat, sigma_hat) — Fréchet mean
    approximation for well-separated clusters. Zhang (2017) Ch.8; Selim (1984).
    Returns 1-indexed integer array of cluster labels (matches R convention).
    """
    if rng is None:
        rng = np.random.default_rng()
    mu    = params["mu_hat"]
    sigma = params["sigma_hat"]
    n     = len(mu)

    best_labels  = np.zeros(n, dtype=int)
    best_inertia = np.inf

    for _ in range(n_init):
        init_idx      = rng.choice(n, size=k, replace=False)
        centers_mu    = mu[init_idx].copy()
        centers_sigma = sigma[init_idx].copy()
        labels        = np.zeros(n, dtype=int)
        dists         = np.empty((n, k))

        for _ in range(max_iter):
            for cl in range(k):
                dists[:, cl] = np.array([
                    fisher_rao_univariate(mu[i], sigma[i], centers_mu[cl], centers_sigma[cl])
                    for i in range(n)
                ])
            new_labels = np.argmin(dists, axis=1)

            if np.array_equal(new_labels, labels):
                labels = new_labels
                break
            labels = new_labels

            for cl in range(k):
                mask = labels == cl
                if mask.any():
                    centers_mu[cl]    = mu[mask].mean()
                    centers_sigma[cl] = sigma[mask].mean()

        inertia = np.sum(dists[np.arange(n), labels] ** 2)
        if inertia < best_inertia:
            best_inertia = inertia
            best_labels  = labels + 1          # convert to 1-indexed

    return best_labels


# --- Hierarchical clustering -------------------------------------------------

def hclust_custom(
    dist_matrix: np.ndarray, k: int, method: str = "complete"
) -> np.ndarray:
    """Hierarchical clustering from a precomputed distance matrix.

    Returns 1-indexed integer array of cluster labels.
    """
    condensed = squareform(dist_matrix)
    Z         = linkage(condensed, method=method)
    return fcluster(Z, t=k, criterion="maxclust")


# --- Accuracy with optimal label matching ------------------------------------

def match_accuracy(true_labels: np.ndarray, pred_labels: np.ndarray) -> float:
    """For k=2: best accuracy over both possible label assignments."""
    acc = np.mean(pred_labels == true_labels)
    return float(max(acc, 1.0 - acc))


# --- Monte Carlo replication driver ------------------------------------------

def run_replications(
    mu_list: list[float],
    sigma_list: list[float],
    k: int = 2,
    t: int = 100,
    n: int = 30,
    n_rep: int = 100,
    hclust_method: str = "complete",
    seed: int = 42,
) -> dict[str, np.ndarray]:
    """Run n_rep Monte Carlo replications; return dict of accuracy arrays."""
    rng     = np.random.default_rng(seed)
    km_fr   = np.empty(n_rep)
    km_eu   = np.empty(n_rep)
    hc_fr   = np.empty(n_rep)
    hc_eu   = np.empty(n_rep)

    from sklearn.cluster import KMeans  # noqa: PLC0415

    for r in range(n_rep):
        dat         = generate_dataset(mu_list, sigma_list, t=t, n=n, rng=rng)
        true_labels = dat["cluster"]
        pts         = np.column_stack([dat["mu_hat"], dat["sigma_hat"]])

        fr_dist = fisher_rao_dist_matrix(dat)
        eu_dist = euclidean_dist_matrix(dat)

        km_fr_pred  = kmeans_fr(dat, k=k, rng=rng)
        eu_km_pred  = KMeans(n_clusters=k, n_init=10,
                             random_state=int(rng.integers(1_000_000))).fit_predict(pts) + 1

        km_fr[r] = match_accuracy(true_labels, km_fr_pred)
        km_eu[r] = match_accuracy(true_labels, eu_km_pred)
        hc_fr[r] = match_accuracy(true_labels, hclust_custom(fr_dist, k=k, method=hclust_method))
        hc_eu[r] = match_accuracy(true_labels, hclust_custom(eu_dist, k=k, method=hclust_method))

    return {"km_fr": km_fr, "km_eu": km_eu, "hc_fr": hc_fr, "hc_eu": hc_eu}


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    np.random.seed(42)

    mu_list    = [1.0, 2.0]
    sigma_list = [1.5, 1.5]

    print("Running 100 Monte Carlo replications (k=2, t=100, n=30)…")
    results = run_replications(mu_list, sigma_list)

    zhang_ref = {
        "K-Means + Fisher-Rao":      "0.965 ± 0.001",
        "K-Means + Euclidean":        "0.965 ± 0.010",
        "Hierarchical + Fisher-Rao":  "0.904 ± 0.006",
        "Hierarchical + Euclidean":   "0.922 ± 0.006",
    }

    print(f"\n{'Algorithm':<30}  {'Replicated':>15}  {'Zhang (2017)':>15}")
    print("-" * 65)
    labels_map = {
        "K-Means + Fisher-Rao":      "km_fr",
        "K-Means + Euclidean":        "km_eu",
        "Hierarchical + Fisher-Rao":  "hc_fr",
        "Hierarchical + Euclidean":   "hc_eu",
    }
    n_rep = 100
    for algo, col in labels_map.items():
        arr  = results[col]
        rep  = f"{arr.mean():.3f} ± {arr.std() / n_rep**0.5:.3f}"
        zhang = zhang_ref[algo]
        print(f"{algo:<30}  {rep:>15}  {zhang:>15}")
