#!/bin/bash
# =============================================================
# setup_repo.sh
# Ejecutar UNA sola vez para inicializar el repo y subirlo a GitHub
# Uso: bash setup_repo.sh <tu-usuario-github> <nombre-del-repo>
# Ejemplo: bash setup_repo.sh mauricio statistical-geometry
# =============================================================

GITHUB_USER=${1:-"TU_USUARIO"}
REPO_NAME=${2:-"statistical-geometry"}

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  Setup: Statistical Geometry Repo                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 1. Inicializar git
git init
git branch -M main

# 2. Primer commit
git add .
git commit -m "feat: estructura inicial del proyecto

- Experimentos exp1–exp6 con carpetas R/python/results/notebooks
- README principal con hoja de ruta
- Notas teóricas y de lectura (Costa et al. 2015)
- .gitignore para R y Python
- GitHub Actions CI (lint flake8 + lintr)
- Licencia MIT"

echo ""
echo "✓ Commit inicial creado."
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Ahora crea el repo en GitHub (vacío, sin README):"
echo "  https://github.com/new"
echo ""
echo "  Nombre sugerido: $REPO_NAME"
echo "  Visibilidad: privado o público (tú decides)"
echo "  NO inicialices con README ni .gitignore"
echo "═══════════════════════════════════════════════════════"
echo ""
read -p "  Presiona Enter cuando hayas creado el repo en GitHub..."
echo ""

# 3. Conectar con GitHub y hacer push
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✓ Repo subido a: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Próximos pasos:"
echo "  1. Copia los PDFs a references/"
echo "  2. Empieza con experiments/exp1_distances/R/distances.R"
echo "  3. Crea un branch por experimento: git checkout -b exp1-distances"
echo ""
