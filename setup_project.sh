#!/bin/bash

# Nome do pacote
PKG_NAME="expdespy"

# Criando diretórios principais
mkdir -p src/$PKG_NAME/{models,stats,posthoc,utils,datasets}
mkdir -p tests
mkdir -p examples
mkdir -p docs

# Criando arquivos essenciais
touch README.md
touch LICENSE
touch .gitignore
touch pyproject.toml
touch setup.py

# Inicializando módulos Python
touch src/$PKG_NAME/__init__.py
touch src/$PKG_NAME/models/__init__.py
touch src/$PKG_NAME/stats/__init__.py
touch src/$PKG_NAME/posthoc/__init__.py
touch src/$PKG_NAME/utils/__init__.py
touch src/$PKG_NAME/datasets/__init__.py

# Arquivo de exemplo de teste
cat <<EOF > tests/test_basic.py
def test_dummy():
    assert 1 + 1 == 2
EOF

# Criando README inicial
cat <<EOF > README.md
# $PKG_NAME

**$PKG_NAME** is a Python package for statistical analysis of experimental designs.

## Features

- Completely Randomized Design (DIC)
- Randomized Block Design (DBC)
- Split-Plot Design
- ANOVA
- Assumption checks
- Post-hoc tests: Tukey, Duncan, Scott-Knott
- Visualizations with significance letters

## Install

\`\`\`bash
pip install .
\`\`\`

## Usage

\`\`\`python
from $PKG_NAME.models import DIC
dic = DIC(data=df, response="yield", treatment="fertilizer")
dic.anova()
dic.tukey()
dic.plot_means()
\`\`\`

## License

MIT
EOF

# Adicionando setup.py (opcional para compatibilidade legacy)
cat <<EOF > setup.py
from setuptools import setup, find_packages

setup(
    name="$PKG_NAME",
    version="0.1.0",
    description="Statistical analysis of experimental designs in Python",
    author="Seu Nome",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "statsmodels",
        "scikit-posthocs",
        "matplotlib",
        "seaborn"
    ],
)
EOF

# pyproject.toml (moderno, recomendado pelo PEP 621)
cat <<EOF > pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "$PKG_NAME"
version = "0.1.0"
description = "Python package for experimental design analysis (ExpDes-like)"
authors = [{ name="Seu Nome", email="seu@email.com" }]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = [
    "pandas",
    "numpy",
    "scipy",
    "statsmodels",
    "scikit-posthocs",
    "matplotlib",
    "seaborn"
]

[tool.setuptools.packages.find]
where = ["src"]
EOF

# Criando .gitignore padrão
cat <<EOF > .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv
*.egg-info/
dist/
build/
.ipynb_checkpoints/
EOF

echo "✅ Estrutura do pacote $PKG_NAME criada com sucesso!"