from setuptools import setup, find_packages

setup(
    name="expdespy",
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
