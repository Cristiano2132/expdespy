import re
from pathlib import Path
from setuptools import setup, find_packages

def get_version():
    """
    Lê a versão diretamente do pyproject.toml para evitar duplicação.
    """
    content = Path("pyproject.toml").read_text()
    match = re.search(r'^version\s*=\s*["\'](.+)["\']', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Não foi possível encontrar a versão no pyproject.toml")

setup(
    name="expdespy",
    version=get_version(),
    description="Statistical analysis of experimental designs in Python",
    author="Cristiano F. Oliveira",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas==2.2.2",
        "numpy==1.26.4",
        "scipy==1.12.0",
        "statsmodels==0.14.1",
        "scikit-posthocs",  # mantido genérico
        "matplotlib==3.8.4",
        "seaborn==0.13.2",
        "tabulate==0.9.0"
    ],
)