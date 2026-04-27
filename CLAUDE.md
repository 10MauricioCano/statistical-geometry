# CLAUDE.md — Project Guide for AI-Assisted Development

This file is the primary reference for Claude (and any AI assistant) working
on this project. Read it fully before writing any code or answering any question.

---

## 1. Project Overview

We are **replicating and extending** the experiments from:

> Bo Zhang (2017). *Machine Learning on Statistical Manifold*.
> Harvey Mudd College Senior Thesis. Advisor: Weiqing Gu.

The thesis applies information geometry to machine learning — specifically,
replacing the Euclidean distance with statistically meaningful distances
(Fisher-Rao, Hellinger) when clustering and classifying probability distributions.

The theoretical foundation comes from:

> Costa, Santos, Strapasson (2015). *Fisher information distance: A geometrical reading*.
> Discrete Applied Mathematics, 197, 59–69.

And the broader framework is extended by:

> Fraiman, Moreno, Ransford (2023). *A Cramér–Wold theorem for elliptical distributions*.
> Journal of Multivariate Analysis, 196, 105176.

**Current scope**: replicating Zhang (2017) experiments in order, exp1 → exp6.
No extensions yet. Stay faithful to the thesis parameters unless explicitly told otherwise.

---

## 2. Working Environment

| Tool | Details |
|------|---------|
| Primary language | **R** (experiments exp1–exp6) |
| Secondary language | **Python** (same experiments, parallel implementation) |
| R environment | RStudio — terminal and script editor |
| Python environment | VS Code or RStudio terminal |
| Version control | Git / GitHub (`github.com/10MauricioCano/statistical-geometry`) |
| OS | Windows 11 (PowerShell + Git Bash available) |
| Shell for scripts | **Git Bash** — use `bash` syntax, not PowerShell |

### Important shell notes
- The user works in **RStudio's built-in terminal** or **VS Code terminal**
- Do NOT suggest `wsl` or assume Linux is available natively
- Git Bash is available for `.sh` scripts
- For R code: always give runnable `.R` files, not just console snippets
- For Python: standard `venv` or base install, no conda assumed

---

## 3. Repository Structure

```
statistical-geometry/
│
├── CLAUDE.md                        ← this file
├── README.md                        ← project overview for humans
├── LICENSE                          ← MIT
├── .gitignore                       ← R + Python
│
├── experiments/
│   ├── exp1_distances/              ← statistical distance functions
│   ├── exp2_clustering_univariate_k2/
│   ├── exp3_clustering_univariate_k3/
│   ├── exp4_clustering_bivariate/
│   ├── exp5_poisson_hellinger/
│   └── exp6_convergence/
│       └── (each has: R/ python/ results/ notebooks/)
│
├── notes/
│   ├── theory/                      ← conceptual notes, math
│   ├── readings/                    ← per-paper annotations
│   └── scratch/                     ← working ideas
│
└── references/                      ← source PDFs
```

Each experiment folder follows this internal convention:

```
expN_name/
├── README.md          ← objective, parameters, expected results
├── R/
│   └── *.R            ← source functions (NOT scripts with side effects)
├── python/
│   └── *.py           ← mirror implementation
├── notebooks/
│   └── *.Rmd or *.ipynb
└── results/
    └── figures/, tables/
```

---

## 4. Experiment Roadmap

Work through experiments **strictly in order**. Each one depends on the previous.

### Exp 1 — Statistical Distance Functions
**Goal**: implement and sanity-check the three core distances.
**Status**: 🔲 Not started
**Branch**: `exp1-distances`

Distances to implement:

**Fisher-Rao univariate** (Costa et al. 2015, eq. 9 / Zhang 2017, eq. 4.11):
$$d_F(P,Q) = \sqrt{2}\ln\!\left(\frac{\mathcal{F}(P,Q) + (\mu_1-\mu_2)^2 + 2(\sigma_1^2+\sigma_2^2)}{4\sigma_1\sigma_2}\right)$$
where $\mathcal{F} = \sqrt{[(\mu_1-\mu_2)^2+2(\sigma_1-\sigma_2)^2][(\mu_1-\mu_2)^2+2(\sigma_1+\sigma_2)^2]}$

Special case (same mean): $d_F = \sqrt{2}|\ln(\sigma_2/\sigma_1)|$

**Fisher-Rao bivariate diagonal** (Zhang 2017, eq. 4.12 / 8.2):
$$d_F(\theta_1,\theta_2) = \sqrt{2\sum_{i=1}^{2}\left(\ln\frac{\|(\frac{\mu_1}{\sqrt{2}},\sigma_{1i})-(\frac{\mu_2}{\sqrt{2}},-\sigma_{2i})\|+\|(\frac{\mu_1}{\sqrt{2}},\sigma_{1i})-(\frac{\mu_2}{\sqrt{2}},\sigma_{2i})\|}{\|(\frac{\mu_1}{\sqrt{2}},\sigma_{1i})-(\frac{\mu_2}{\sqrt{2}},-\sigma_{2i})\|-\|(\frac{\mu_1}{\sqrt{2}},\sigma_{1i})-(\frac{\mu_2}{\sqrt{2}},\sigma_{2i})\|}\right)^2}$$

**Hellinger discrete** (Zhang 2017, eq. 5.1):
$$d_H(p,q) = \sqrt{\frac{1}{2}\sum_{j=0}^{k}(\sqrt{p_j}-\sqrt{q_j})^2}$$

Sanity checks required:
- $d(P, P) = 0$
- $d(P, Q) = d(Q, P)$ (symmetry)
- $d_F((0,1),(0,2)) = \sqrt{2}\ln 2 \approx 0.9802$
- Distances increase as distributions diverge
- $\sigma \to 0$ implies $d_F \to \infty$

---

### Exp 2 — Clustering Univariate Gaussians, k=2
**Goal**: compare k-means and hierarchical clustering with Euclidean vs Fisher-Rao.
**Status**: 🔲 Not started — requires exp1
**Branch**: `exp2-clustering-k2`

**Exact parameters from Zhang (2017), Table 8.1–8.2**:
- $k = 2$ clusters
- True distributions: $(\mu_1, \sigma_1) = (1, 1.5)$ and $(\mu_2, \sigma_2) = (2, 1.5)$
- $t = 100$ empirical distributions per cluster (each estimated from $n = 30$ samples)
- 100 Monte Carlo replications
- Metric: accuracy = $1 - \text{misclassified}/\text{total}$

**Data generation process** (Zhang, Ch. 7):
1. Fix true $(\mu_k, \sigma_k)$ for each cluster $k$
2. For each of $t$ repetitions: draw $n$ samples from $\mathcal{N}(\mu_k, \sigma_k^2)$,
   estimate $(\hat\mu_k, \hat\sigma_k)$ from those samples
3. The object to cluster is the set of all $k \times t$ estimated distributions in parameter space

**Expected results (Table 8.1)**:
| Algorithm | Accuracy |
|-----------|----------|
| Hierarchical + Fisher-Rao | 0.904 ± 0.006 |
| Hierarchical + Euclidean | 0.922 ± 0.006 |
| K-Means + Fisher-Rao | 0.965 ± 0.001 |
| K-Means + Euclidean | 0.965 ± 0.010 |

---

### Exp 3 — Clustering Univariate Gaussians, k=3
**Goal**: same setup as exp2, increase k to see metric advantage emerge.
**Status**: 🔲 Not started — requires exp2
**Branch**: `exp3-clustering-k3`

**Parameters**: same as exp2 but $k=3$. Choose 3 well-separated true distributions.
The thesis doesn't specify exact parameters for k=3 univariate — choose them
so clusters are meaningfully separated but not trivially obvious.

**Expected pattern**:
- K-Means + Fisher-Rao wins in ~98/100 replications vs Euclidean
- Hierarchical + Fisher-Rao wins in ~70/100 replications vs Euclidean

---

### Exp 4 — Clustering Bivariate Gaussians, k=3
**Goal**: extend to 3D parameter space $(\mu, \sigma_1, \sigma_2)$ with diagonal covariance.
**Status**: 🔲 Not started — requires exp1 (bivariate Fisher-Rao)
**Branch**: `exp4-clustering-bivariate`

**Exact parameters from Zhang (2017), Section 8.3**:
- $k = 3$, $t = 100$, $n = 30$, 100 replications
- True distributions: $(\mu, \sigma_1, \sigma_2) = (1,1,2),\ (1.5,1.5,2.5),\ (2,2,3)$
- Diagonal covariance: $\Sigma = \text{diag}(\sigma_1^2, \sigma_2^2)$, same $\mu$ for both components

**Expected results (Table 8.3)**:
| Algorithm | Accuracy |
|-----------|----------|
| Hierarchical + Fisher-Rao | 0.860 ± 0.008 |
| Hierarchical + Euclidean | 0.716 ± 0.012 |
| K-Means + Fisher-Rao | 0.937 ± 0.001 |
| K-Means + Euclidean | 0.877 ± 0.003 |

---

### Exp 5 — Clustering Poisson Distributions with Hellinger
**Goal**: apply clustering to discrete distributions; include MDS visualization.
**Status**: 🔲 Not started — requires exp1 (Hellinger distance)
**Branch**: `exp5-poisson-hellinger`

**Exact parameters from Zhang (2017), Section 9**:
- $k = 3$ Poisson clusters: $\lambda_1=6,\ \lambda_2=8,\ \lambda_3=10$
- 100 empirical distributions per cluster, each from $n=30$ data points
- 100 replications
- Truncate Poisson at reasonable upper bound (e.g., max observed value + buffer)

**Expected results (Table 9.1)**:
| Algorithm | Accuracy |
|-----------|----------|
| Hierarchical + Hellinger | 0.792 ± 0.010 |
| Hierarchical + Euclidean | 0.674 ± 0.008 |
| K-Means + Hellinger | 0.922 ± 0.004 |
| K-Means + Euclidean | 0.901 ± 0.004 |

Also produce: MDS plot projecting distributions to 2D using Hellinger distance matrix.

---

### Exp 6 — Convergence and Optimality of K-Means with Hellinger
**Goal**: verify empirically that k-means + Hellinger converges to a local minimum.
**Status**: 🔲 Not started — requires exp5
**Branch**: `exp6-convergence`

**What to show**:
1. Plot objective function $F$ vs iteration number — must decrease monotonically and plateau
2. Record number of iterations to convergence across replications
3. Verify the centroid formula (Zhang eq. 10.12):
$$z^*_t = \frac{2\sum_j a_j \sqrt{x_{jt}}}{\sum_j a_j}$$
4. Compare convergence speed: Hellinger vs Euclidean k-means

Theoretical basis: Selim & Ismail (1984) Theorem + Zhang Ch. 10 proof that
$A(W^*)$ is a singleton for Hellinger centroid → local minimum guaranteed.

---

## 5. Coding Standards

### R
- Use `set.seed(42)` at the top of every script that generates random data
- Functions go in `R/` files; scripts that run experiments go in `notebooks/` (.Rmd)
- Name functions descriptively: `fisher_rao_univariate()`, `generate_clusters()`, `run_kmeans_stat()`
- Return data frames from experiment functions, not just print output
- Use `ggplot2` for all plots; save to `results/figures/` with `ggsave()`
- Required packages: `ggplot2`, `cluster`, `MASS`

```r
# Standard file header
# ============================================================
# File: R/distances.R
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4; Costa et al. (2015)
# ============================================================
```

### Python
- Mirror the R implementation function by function
- Use `numpy`, `scipy`, `matplotlib`, `scikit-learn`
- Type hints on all functions
- Docstrings with formula reference (e.g., `Zhang 2017, eq. 4.11`)

```python
# ============================================================
# File: python/distances.py
# Experiment: exp1_distances
# Description: Core statistical distance functions
# Reference: Zhang (2017) Ch.4; Costa et al. (2015)
# ============================================================
```

### General rules
- **Never hardcode parameters** — pass them as function arguments with defaults matching Zhang
- **Always match Zhang's exact parameters** when replicating — do not simplify
- **Reproduce tables first** — get numbers close to Zhang's before any visualization
- **Comment every non-obvious formula** with equation number from the source

---

## 6. Git Workflow

```bash
# Start a new experiment
git checkout main
git pull
git checkout -b exp1-distances

# Work, commit frequently
git add experiments/exp1_distances/R/distances.R
git commit -m "exp1: implement fisher_rao_univariate() with sanity checks"

# When experiment is complete and results match Zhang
git push origin exp1-distances
# Open Pull Request on GitHub → merge to main
```

**Commit message format**:
```
exp1: short description of what was done

Optional longer body if needed.
```

**Branch naming**: `exp1-distances`, `exp2-clustering-k2`, etc.

---

## 7. Key Mathematical Reference

### The data generation pipeline (Zhang, Ch. 7)
This is the core procedure used in exp2–exp5:

```
For each cluster k in 1..K:
  Fix true parameters θ_k = (μ_k, σ_k)
  For each repetition i in 1..t:
    Draw n samples from N(μ_k, σ_k²)
    Estimate θ̂_k^(i) = (sample_mean, sample_sd)
    → This is one point in parameter space

Object to cluster = all K×t estimated points (unlabeled)
Ground truth = which cluster each point came from
```

Key parameters and their roles:
- `k` — number of true clusters
- `t` — number of empirical distributions per cluster (cluster "size")
- `n` — samples per empirical distribution (controls cluster "tightness")
- Larger `n` → tighter clusters → easier problem

### Accuracy metric (Zhang, Ch. 8)
$$\text{accuracy} = 1 - \frac{\text{number of misclassified elements}}{\text{total elements}}$$

Report as mean ± standard error across 100 replications.

### Centroid on statistical manifold (Zhang, Ch. 6)
For Fisher-Rao: centroid is NOT the arithmetic mean of parameters.
It requires iterative geodesic averaging (Fréchet mean).
For Hellinger (discrete): closed form exists — see eq. 10.12.

---

## 8. How to Interact with Claude on This Project

When asking Claude for help, use these patterns for best results:

**Starting a new experiment file**:
> "We're in exp1. Write `R/distances.R` with the three distance functions.
> Use the exact formulas from Section 4 of the roadmap in CLAUDE.md."

**Debugging a result that doesn't match Zhang**:
> "My k-means accuracy is 0.91 but Zhang reports 0.965 for exp2.
> Here is my current code: [paste]. What could be wrong?"

**Asking for explanation before coding**:
> "Before we code exp4, explain how the bivariate Fisher-Rao formula
> (eq. 4.12) reduces to the univariate case when p=1."

**Asking for the next step**:
> "exp2 R implementation is done and matches Table 8.1.
> What should we do next?"

Claude will always:
- Check CLAUDE.md before suggesting anything
- Respect the experiment order
- Flag if a suggestion deviates from Zhang's exact setup
- Produce complete, runnable files (not fragments)
- Use English in all code, comments, and technical explanations

---

## 9. Progress Tracker

Update this table as experiments are completed.

| Exp | R impl | Python impl | Results match Zhang | Notes |
|-----|--------|-------------|--------------------:|-------|
| exp1 | 🔲 | 🔲 | 🔲 | |
| exp2 | 🔲 | 🔲 | 🔲 | |
| exp3 | 🔲 | 🔲 | 🔲 | |
| exp4 | 🔲 | 🔲 | 🔲 | |
| exp5 | 🔲 | 🔲 | 🔲 | |
| exp6 | 🔲 | 🔲 | 🔲 | |

---

## 10. References

| Label | Full citation |
|-------|---------------|
| Zhang 2017 | Zhang, B. (2017). *Machine Learning on Statistical Manifold*. HMC Senior Thesis. |
| Costa 2015 | Costa, S.I.R., Santos, S.A., Strapasson, J.E. (2015). Fisher information distance: A geometrical reading. *Discrete Applied Mathematics*, 197, 59–69. |
| Fraiman 2023 | Fraiman, R., Moreno, L., Ransford, T. (2023). A Cramér–Wold theorem for elliptical distributions. *Journal of Multivariate Analysis*, 196, 105176. |
| Selim 1984 | Selim, S.Z., Ismail, M.A. (1984). K-means-type algorithms. *IEEE TPAMI*, 6(1), 81–87. |
