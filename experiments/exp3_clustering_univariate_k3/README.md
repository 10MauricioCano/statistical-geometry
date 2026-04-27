# Exp 3 — Clustering univariado k=3

## Objetivo

Mismo esquema que exp2 pero con tres familias. Aquí se espera que
la ventaja de la métrica Fisher-Rao sea visible y estadísticamente significativa.

## Configuración (Zhang, 2017, Sección 8.2)

- k = 3 clusters
- n = 30, t = 100, 100 réplicas
- Parámetros de los tres clusters a definir

## Resultado esperado

- k-means Fisher-Rao supera k-means Euclidiano en ~98/100 corridas
- Jerárquico Fisher-Rao supera Euclidiano en ~70/100 corridas

## Archivos

- `R/clustering_k3.R`
- `python/clustering_k3.py`
- `results/`
