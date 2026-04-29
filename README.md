# Statistical Geometry — Machine Learning on Statistical Manifolds

Two intertwined objectives:

1. **Replicate Zhang (2017)** — implement the information-geometry clustering experiments, replacing Euclidean distance with Fisher-Rao and Hellinger distances when working with probability distributions.
2. **Build a production ML system** — apply the full ML lifecycle framework from Chip Huyen (2022): data engineering, feature engineering, model development, deployment, monitoring, and MLOps infrastructure.

The geometric distances from Zhang provide the algorithmic core. Huyen's framework guides how that core is packaged into a reliable, scalable, and maintainable production system.

---

## Background

Standard clustering algorithms use Euclidean distance, which treats distributions as points in parameter space and ignores their shape. Fisher-Rao and Hellinger distances are *intrinsic* to the distribution family: they measure how hard it is to statistically distinguish two distributions, not how far apart their parameters are numerically. The thesis shows this distinction matters — often substantially — in clustering accuracy.

Grounded in three primary papers:

| # | Reference | Topic |
|---|---|---|
| 1 | Costa, Santos, Strapasson (2015) | Fisher information distance and hyperbolic geometry |
| 2 | Zhang (2017) | Clustering and classification on statistical manifolds |
| 3 | Fraiman, Moreno, Ransford (2023) | Cramér-Wold theorem for elliptical distributions |

---

## Experiment Roadmap

Work proceeds strictly in order — each experiment builds on the previous.

| Experiment | Description | Status |
|---|---|---|
| exp1 | Fisher-Rao and Hellinger distance functions — implementation and sanity checks | Pending |
| exp2 | Univariate Gaussian clustering k=2: Fisher-Rao vs. Euclidean | Pending |
| exp3 | Univariate Gaussian clustering k=3: Fisher-Rao vs. Euclidean | Pending |
| exp4 | Bivariate Gaussian clustering k=3: 3D parameter space | Pending |
| exp5 | Poisson clustering with Hellinger distance + MDS | Pending |
| exp6 | k-means convergence with Hellinger: monotonicity and local optimality | Pending |

Each experiment reports mean accuracy ± SE across 100 replications, reproducing Zhang's tables before producing any visualization.

---

## Repository Structure

```
statistical-geometry/
├── experiments/
│   ├── exp1_distances/
│   ├── exp2_clustering_univariate_k2/
│   ├── exp3_clustering_univariate_k3/
│   ├── exp4_clustering_bivariate/
│   ├── exp5_poisson_hellinger/
│   └── exp6_convergence/
├── notes/
│   ├── theory/       # Mathematical and conceptual notes
│   ├── readings/     # Notes per paper
│   └── scratch/      # Working drafts
├── references/       # Source paper PDFs
└── .github/
    └── workflows/    # CI: R and Python linting
```

Each experiment follows the same internal layout:

```
expN_name/
├── README.md      # Objective, parameters, expected results
├── R/             # R implementation — pure functions, no side effects at top level
├── python/        # Python implementation — mirrors R function signatures
├── notebooks/     # Jupyter / R Markdown exploratory notebooks
└── results/
    ├── figures/
    └── tables/
```

---

## Setup

### Python

```bash
python -m venv .venv
source .venv/Scripts/activate    # Git Bash on Windows
pip install numpy scipy matplotlib scikit-learn geomstats jupyter
```

### R

```r
install.packages(c("ggplot2", "cluster", "MASS", "rmarkdown"))
```

---

## Stack

`Python` · `R` · `NumPy` · `SciPy` · `geomstats` · `scikit-learn` · `ggplot2` · `GitHub Actions`

---

## Git Workflow

Branch flow: `expN-*` → `develop` → `main`.

```bash
git checkout -b exp1-distances
# ... implement, test, verify against Zhang's tables
git push origin exp1-distances
# open PR: exp1-distances → develop
```

Milestones on `main`: v0.1 (exp1) → v0.2 (exp2+3) → v0.3 (exp4) → v1.0 (exp5+6).

---

## References

- Costa, S.I.R., Santos, S.A., Strapasson, J.E. (2015). *Fisher information distance: A geometrical reading.* Discrete Applied Mathematics, 197, 59–69.
- Zhang, B. (2017). *Machine Learning on Statistical Manifold.* Harvey Mudd College Senior Thesis.
- Fraiman, R., Moreno, L., Ransford, T. (2023). *A Cramér-Wold theorem for elliptical distributions.* Journal of Multivariate Analysis, 196, 105176.
- Huyen, C. (2022). *Designing Machine Learning Systems.* O'Reilly Media. ([companion repo](https://github.com/10MauricioCano/dmls-book))

---

## License

MIT — see [LICENSE](LICENSE)
