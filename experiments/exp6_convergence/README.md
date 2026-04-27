# Exp 6 — Convergencia y optimalidad de k-means con Hellinger

## Objetivo

Verificar empíricamente (y repasar la demostración teórica) de que
el k-means con distancia Hellinger sobre distribuciones de Poisson
converge a un mínimo local, no solo a una solución parcialmente óptima.

## Contexto teórico (Zhang, 2017, Capítulo 10)

El resultado clave es el Teorema 1 (Selim e Ismail, 1984):
si $(W^*, Z^*)$ es una solución parcialmente óptima y $A(W^*)$ es
un singleton, entonces $W^*$ es un mínimo local.

Zhang demuestra que la condición de singleton se satisface para el
centroide de Hellinger (ecuación 10.12), lo que garantiza convergencia
a mínimo local.

## Verificación empírica

- Trazar la evolución de la función objetivo $F$ por iteración
- Confirmar convergencia en número finito de pasos
- Comparar número de iteraciones hasta convergencia: Hellinger vs Euclidiana

## Archivos

- `R/convergence.R`
- `python/convergence.py`
- `notebooks/convergence_analysis.ipynb`
- `results/`
