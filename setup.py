from setuptools import setup, find_packages

setup(
    name="expdespy",
    version="1.0.0",
    description="Statistical analysis of experimental designs in Python",
    author="Cristiano Oliveira",
    author_email="cristiano2132.ufv@gmail.com",  # opcional, substitua se quiser
    url="https://github.com/Cristiano2132/expdespy",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pandas>=1.3",
        "numpy>=1.21",
        "scipy>=1.7",
        "statsmodels>=0.13",
        "scikit-posthocs>=0.6.7",
        "matplotlib>=3.4",
        "seaborn>=0.11"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.10",
)