# Exp 2 — Clustering univariado k=2

## Objetivo

Comparar k-means y clustering jerárquico usando métrica Euclidiana
vs Fisher-Rao sobre dos familias de gaussianas univariadas.

## Configuración (Zhang, 2017, Tabla 8.1)

- k = 2 clusters
- Distribuciones: $(\mu_1, \sigma_1) = (1, 1.5)$ vs $(\mu_2, \sigma_2) = (2, 1.5)$
- n = 30 muestras por distribución, t = 100 distribuciones por cluster
- 100 réplicas Monte Carlo

## Resultado esperado

Con k=2 y clusters bien separados, ambas métricas se comportan de
manera similar (~96% precisión para k-means). Es el experimento de
verificación base.

## Archivos

- `R/clustering_k2.R`
- `python/clustering_k2.py`
- `results/` — tablas de precisión media ± error estándar
