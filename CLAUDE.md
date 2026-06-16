# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

This project has two intertwined objectives:

**1. Replicate Zhang (2017)** — implement the information-geometry experiments from:

> Bo Zhang (2017). *Machine Learning on Statistical Manifold*. Harvey Mudd College Senior Thesis.

The thesis applies information geometry to ML, replacing Euclidean distance with Fisher-Rao and Hellinger distances when clustering probability distributions.

**2. Build a production ML system** — design and implement the full system following:

> Chip Huyen (2022). *Designing Machine Learning Systems*. O'Reilly Media.

The Huyen framework covers the complete ML lifecycle: data engineering, training data, feature engineering, model development, deployment, monitoring, continual learning, and MLOps infrastructure. The geometric distances from Zhang (exp1–exp6) serve as the algorithmic core; Huyen's framework guides how that core is packaged into a reliable, scalable, maintainable, and adaptable production system.

The forked reference repo lives at `github.com/10MauricioCano/dmls-book` (upstream: `github.com/chiphuyen/dmls-book`). It contains chapter summaries, an MLOps tools catalog, and resources — consult it when making system design decisions.

**Immediate scope**: replicate experiments exp1 → exp6 in order. Stay faithful to Zhang's exact parameters unless explicitly told otherwise. System design work (Huyen) follows once the algorithmic layer is verified.

---

## Commands

### R

```bash
# Source a function file (no side effects — functions only)
Rscript -e "source('experiments/exp1_distances/R/distances.R')"

# Run an experiment notebook
Rscript -e "rmarkdown::render('experiments/exp1_distances/notebooks/exp1.Rmd')"

# Install required packages (run once)
Rscript -e "install.packages(c('ggplot2', 'cluster', 'MASS', 'rmarkdown'))"

# Lint a file
Rscript -e "lintr::lint('experiments/exp1_distances/R/distances.R')"
```

### Python

```bash
# Set up venv (run once, from repo root)
python -m venv .venv
source .venv/Scripts/activate          # Git Bash on Windows
pip install numpy scipy matplotlib scikit-learn jupyter

# Run a script
python experiments/exp1_distances/python/distances.py
```

### Shell note
Use **Git Bash** syntax for all shell commands. Do NOT use WSL or PowerShell syntax. The user is on Windows 11.

---

## Repository Structure

Each experiment follows this layout:

```
experiments/expN_name/
├── README.md          ← objective, parameters, expected results
├── R/
│   └── *.R            ← pure functions (NO side effects at top level)
├── python/
│   └── *.py           ← mirrors the R implementation
├── notebooks/
│   └── *.Rmd or *.ipynb
└── results/
    └── figures/, tables/
```

---

## Cross-Experiment Dependencies

Experiments exp2–exp6 call functions from exp1. **knitr sets the working directory to the notebook's own folder**, so paths in `.Rmd` files are relative to `notebooks/`. R/ function files contain no `source()` calls — the notebook is the sole entry point.

**R** (from a notebook at `expN_*/notebooks/`):
```r
source("../../exp1_distances/R/distances.R")   # 2 levels up to experiments/
source("../R/data_generation.R")               # sibling R/ folder
```

**Python** (from `expN_*/python/`, uses `__file__` so path is always correct):
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../exp1_distances/python"))
from distances import fisher_rao_univariate, fisher_rao_bivariate, hellinger_discrete
```

**exp1 function API**:
```
# R
fisher_rao_univariate(mu1, sigma1, mu2, sigma2)   # scalars → scalar
fisher_rao_bivariate(mu1, sigma1, mu2, sigma2)    # sigma = c(s1, s2) → scalar
hellinger_discrete(p, q)                          # vectors → scalar, auto-normalizes

# Python (same names; sigma1/sigma2 are np.ndarray of length 2 for bivariate)
```

---

## Experiment Roadmap

Work **strictly in order** — each experiment depends on the previous.

### Exp 1 — Statistical Distance Functions
**Branch**: `exp1-distances`

Implement three distance functions:

**Fisher-Rao univariate** (Costa 2015 eq.9 / Zhang eq.4.11):
```
d_F(P,Q) = sqrt(2) * ln( (F + (μ1-μ2)² + 2(σ1²+σ2²)) / (4σ1σ2) )
where F = sqrt( [(μ1-μ2)²+2(σ1-σ2)²] * [(μ1-μ2)²+2(σ1+σ2)²] )
Same-mean special case: d_F = sqrt(2)*|ln(σ2/σ1)|
```

**Fisher-Rao bivariate diagonal** (Zhang eq.4.12 / 8.2):
```
d_F(θ1,θ2) = sqrt( 2 * sum_{i=1}^{2} [ln((A_i + B_i)² / (4·σ1i·σ2i))]² )
where Δμ = (μ1 - μ2) / sqrt(2)
      A_i = sqrt( Δμ² + (σ1i + σ2i)² )
      B_i = sqrt( Δμ² + (σ1i - σ2i)² )
Numerically stable: avoids A² - B² cancellation when σ1i ≈ σ2i.
```

**Hellinger discrete** (Zhang eq.5.1):
```
d_H(p,q) = sqrt( (1/2) * sum_j (sqrt(p_j) - sqrt(q_j))² )
```

Required sanity checks:
- `d(P, P) == 0`
- `d(P, Q) == d(Q, P)`
- `d_F((0,1),(0,2)) ≈ 0.9802` (= sqrt(2)*ln2)
- Distances increase as distributions diverge
- `σ → 0` implies `d_F → ∞`

---

### Exp 2 — Clustering Univariate Gaussians, k=2
**Branch**: `exp2-clustering-k2`  |  Requires: exp1

**Files**: `R/data_generation.R` (stub exists) + `R/clustering_k2.R` (main experiment); `python/clustering_k2.py`.

**Parameters (Zhang Table 8.1)**:
- k=2, t=100 distributions/cluster, n=30 samples/distribution, 100 replications
- True params: (μ1,σ1)=(1,1.5) and (μ2,σ2)=(2,1.5)

**Accuracy (Zhang Table 8.1 vs replicated, seed=42, 100 reps)**:
| Algorithm | Zhang (2017) | Replicated |
|-----------|--------------|------------|
| K-Means + Fisher-Rao      | 0.965 ± 0.001 | 0.966 ± 0.001 |
| K-Means + Euclidean       | 0.965 ± 0.010 | 0.966 ± 0.001 |
| Hierarchical + Fisher-Rao | 0.904 ± 0.006 | 0.916 ± 0.006 |
| Hierarchical + Euclidean  | 0.922 ± 0.006 | 0.916 ± 0.007 |

K-Means values match exactly. Hierarchical is ~1% higher with FR/Euclidean ordering swapped — consistent with Monte Carlo variance and possibly a different linkage method in the original (we use `complete`).

---

### Exp 3 — Clustering Univariate Gaussians, k=3
**Branch**: `exp3-clustering-k3`  |  Requires: exp2

Same setup as exp2 but k=3. Thesis does not specify exact parameters for k=3 univariate — choose 3 well-separated but non-trivial distributions.

**Expected pattern**: K-Means + Fisher-Rao wins ~98/100 replications; Hierarchical + Fisher-Rao wins ~70/100.

---

### Exp 4 — Clustering Bivariate Gaussians, k=3
**Branch**: `exp4-clustering-bivariate`  |  Requires: exp1 (bivariate formula)

**Parameters (Zhang Section 8.3)**:
- k=3, t=100, n=30, 100 replications
- True params: (μ,σ1,σ2) = (1,1,2), (1.5,1.5,2.5), (2,2,3)
- Diagonal covariance Σ = diag(σ1², σ2²), same μ for both components

**Expected accuracy (Table 8.3)**:
| Algorithm | Accuracy |
|-----------|----------|
| Hierarchical + Fisher-Rao | 0.860 ± 0.008 |
| Hierarchical + Euclidean  | 0.716 ± 0.012 |
| K-Means + Fisher-Rao      | 0.937 ± 0.001 |
| K-Means + Euclidean       | 0.877 ± 0.003 |

---

### Exp 5 — Clustering Poisson with Hellinger
**Branch**: `exp5-poisson-hellinger`  |  Requires: exp1 (Hellinger)

**Parameters (Zhang Section 9)**:
- k=3, λ1=6, λ2=8, λ3=10; t=100, n=30, 100 replications
- Truncate Poisson support at max observed value + buffer

**Expected accuracy (Table 9.1)**:
| Algorithm | Accuracy |
|-----------|----------|
| Hierarchical + Hellinger | 0.792 ± 0.010 |
| Hierarchical + Euclidean | 0.674 ± 0.008 |
| K-Means + Hellinger      | 0.922 ± 0.004 |
| K-Means + Euclidean      | 0.901 ± 0.004 |

Also produce: MDS plot projecting distributions to 2D using Hellinger distance matrix.

---

### Exp 6 — Convergence of K-Means with Hellinger
**Branch**: `exp6-convergence`  |  Requires: exp5

1. Plot objective function F vs. iteration — must decrease monotonically and plateau
2. Record iterations to convergence across replications
3. Verify Hellinger centroid formula (Zhang eq.10.12): `z*_t = 2*sum(a_j * sqrt(x_jt)) / sum(a_j)`
4. Compare convergence speed: Hellinger vs Euclidean k-means

---

## Data Generation Pipeline (Zhang Ch.7)

Used in exp2–exp5:

```
For each cluster k = 1..K:
  Fix true θ_k = (μ_k, σ_k)
  For each repetition i = 1..t:
    Draw n samples from N(μ_k, σ_k²)
    Estimate θ̂_k^(i) = (sample_mean, sample_sd)   ← one point in parameter space

Object to cluster = all K×t estimated points (unlabeled)
Ground truth      = which cluster each point came from
```

**Accuracy** = 1 − misclassified/total. Report mean ± SE across 100 replications.

**Centroid note**: For Fisher-Rao, the centroid is the Fréchet mean (iterative geodesic average), NOT the arithmetic mean of parameters. For Hellinger, a closed form exists (eq.10.12).

---

## Coding Standards

### R
- `set.seed(42)` at top of every script generating random data
- `R/` files contain only function definitions — no side effects at top level
- Notebooks (`.Rmd`) are the entry points that call those functions
- `ggplot2` for all plots; save with `ggsave()` to `results/figures/`
- Return data frames, not printed output
- Required packages: `ggplot2`, `cluster`, `MASS`

Standard file header:
```r
# ============================================================
# File: R/distances.R
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4; Costa et al. (2015)
# ============================================================
```

### Python
- Mirror R function signatures exactly
- Type hints on all functions
- Docstring must cite equation (e.g., `Zhang 2017, eq. 4.11`)
- Required packages: `numpy`, `scipy`, `matplotlib`, `scikit-learn`

Standard file header:
```python
# ============================================================
# File: python/distances.py
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4; Costa et al. (2015)
# ============================================================
```

### Both languages
- Never hardcode parameters — pass as function arguments with Zhang defaults
- Comment every non-obvious formula with its equation number from the source
- Reproduce Zhang's tables before writing any visualization code

---

## Git Workflow

Branch flow: `expN-*` → `develop` → `main` (one direction only).

```bash
# Start an experiment
git checkout develop && git pull origin develop
git checkout -b exp1-distances

# Commit format
git commit -m "exp1(R): implement fisher_rao_univariate() — passes sanity checks"
# scope(lang): description
# scope = exp1..exp6 | docs | infra
# lang  = R | python | omit if both

# Finish → open PR on GitHub: expN-* → develop (squash merge)
git push origin exp1-distances
```

Milestones on `main`: v0.1 (exp1), v0.2 (exp2+3), v0.3 (exp4), v1.0 (exp5+6).

---

## Progress Tracker

| Exp | R impl | Python impl | Results match Zhang | Notes |
|-----|--------|-------------|---------------------|-------|
| exp1 | ✅ | ✅ | ✅ | Merged to main (v0.1) |
| exp2 | ✅ | ✅ | ✅ | Results match Zhang Table 8.1 |
| exp3 | 🔲 | 🔲 | 🔲 | |
| exp4 | 🔲 | 🔲 | 🔲 | |
| exp5 | 🔲 | 🔲 | 🔲 | |
| exp6 | 🔲 | 🔲 | 🔲 | |

---

## References

| Label | Citation |
|-------|----------|
| Zhang 2017 | Zhang, B. (2017). *Machine Learning on Statistical Manifold*. HMC Senior Thesis. |
| Huyen 2022 | Huyen, C. (2022). *Designing Machine Learning Systems*. O'Reilly Media. Fork: github.com/10MauricioCano/dmls-book |
| Costa 2015 | Costa, S.I.R., Santos, S.A., Strapasson, J.E. (2015). Fisher information distance: A geometrical reading. *Discrete Applied Mathematics*, 197, 59–69. |
| Fraiman 2023 | Fraiman, R., Moreno, L., Ransford, T. (2023). A Cramér–Wold theorem for elliptical distributions. *Journal of Multivariate Analysis*, 196, 105176. |
| Selim 1984 | Selim, S.Z., Ismail, M.A. (1984). K-means-type algorithms. *IEEE TPAMI*, 6(1), 81–87. |
