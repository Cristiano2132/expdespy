from setuptools import setup, find_packages

setup(
    name="expdespy",
    version="1.0.0",
    description="Statistical analysis of experimental designs in Python",
    author="Seu Nome",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas==2.2.2",
        "numpy==1.26.4",
        "scipy==1.12.0",
        "statsmodels==0.14.1",
        "scikit-posthocs",  # não aparece no seu requirements.txt, mantenha genérico
        "matplotlib==3.8.4",
        "seaborn==0.13.2",
        "tabulate==0.9.0"
    ],
)
