# Exp 5 — Clustering de distribuciones de Poisson con Hellinger

## Objetivo

Aplicar clustering a distribuciones discretas de Poisson usando la
distancia de Hellinger. Incluye visualización con escalado multidimensional (MDS).

## Configuración (Zhang, 2017, Sección 9)

- k = 3 clusters de distribuciones de Poisson
- Parámetros: $\lambda_1 = 6,\ \lambda_2 = 8,\ \lambda_3 = 10$
- 100 distribuciones empíricas por cluster, 30 puntos por distribución
- 100 réplicas

## Resultado esperado (Tabla 9.1)

| Algoritmo | Precisión |
|-----------|-----------|
| Jerárquico + Hellinger | 0.792 ± 0.010 |
| Jerárquico + Euclidiana | 0.674 ± 0.008 |
| K-Means + Hellinger | 0.922 ± 0.004 |
| K-Means + Euclidiana | 0.901 ± 0.004 |

## Archivos

- `R/poisson_hellinger.R`
- `python/poisson_hellinger.py`
- `notebooks/mds_visualization.ipynb`
- `results/`
