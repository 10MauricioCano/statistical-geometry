# Statistical Geometry — Machine Learning on Statistical Manifolds

Exploración práctica de geometría de la información y sus aplicaciones en machine learning,
siguiendo los tres artículos fundacionales del proyecto:

| # | Referencia | Tema central |
|---|-----------|--------------|
| 1 | Costa, Santos, Strapasson (2015) | Distancia de Fisher y geometría hiperbólica |
| 2 | Zhang, Bo (2017) | Clustering y clasificación en variedades estadísticas |
| 3 | Fraiman, Moreno, Ransford (2023) | Teorema de Cramér-Wold para distribuciones elípticas |

---

## Estructura del repositorio

```
statistical-geometry/
│
├── experiments/
│   ├── exp1_distances/          # Cálculo y verificación de distancias estadísticas
│   ├── exp2_clustering_univariate_k2/   # Clustering gaussianas univariadas, k=2
│   ├── exp3_clustering_univariate_k3/   # Clustering gaussianas univariadas, k=3
│   ├── exp4_clustering_bivariate/       # Clustering gaussianas bivariadas, k=3
│   ├── exp5_poisson_hellinger/          # Clustering Poisson con distancia Hellinger
│   └── exp6_convergence/               # Convergencia y optimalidad de k-means
│
├── notes/
│   ├── theory/      # Apuntes conceptuales y matemáticos
│   ├── readings/    # Notas por artículo
│   └── scratch/     # Ideas y borradores
│
├── references/      # PDFs de los artículos fuente
└── .github/
    └── workflows/   # CI (lint R y Python)
```

Cada experimento tiene la misma estructura interna:

```
expN_nombre/
├── R/           # Implementación en R
├── python/      # Implementación en Python
├── notebooks/   # Jupyter / R Markdown exploratorios
└── results/     # Figuras y tablas generadas
```

---

## Hoja de ruta de experimentos

| Experimento | Descripción | Estado |
|-------------|-------------|--------|
| exp1 | Calcular distancias Fisher-Rao y Hellinger, verificar sanidad | 🔲 Pendiente |
| exp2 | Clustering univariado k=2: Fisher-Rao vs Euclidiana | 🔲 Pendiente |
| exp3 | Clustering univariado k=3: Fisher-Rao vs Euclidiana | 🔲 Pendiente |
| exp4 | Clustering bivariado k=3: espacio de parámetros 3D | 🔲 Pendiente |
| exp5 | Clustering Poisson con Hellinger + MDS | 🔲 Pendiente |
| exp6 | Convergencia k-means con Hellinger: optimalidad local | 🔲 Pendiente |

---

## Requisitos

### R
```r
install.packages(c("ggplot2", "cluster", "MASS", "fields"))
```

### Python
```bash
pip install numpy scipy matplotlib scikit-learn geomstats jupyter
```

---

## Referencias

- Costa, S.I.R., Santos, S.A., Strapasson, J.E. (2015). *Fisher information distance: A geometrical reading*. Discrete Applied Mathematics, 197, 59–69.
- Zhang, B. (2017). *Machine Learning on Statistical Manifold*. Harvey Mudd College Senior Thesis.
- Fraiman, R., Moreno, L., Ransford, T. (2023). *A Cramér–Wold theorem for elliptical distributions*. Journal of Multivariate Analysis, 196, 105176.

---

## Licencia

MIT — ver [LICENSE](LICENSE)
