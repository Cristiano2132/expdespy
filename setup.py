from setuptools import setup, find_packages
from pathlib import Path

install_requires = Path("requirements.txt").read_text().splitlines()


setup(
    name="expdespy",
    version="1.1.0",
    description="Statistical analysis of experimental designs in Python",
    author="Cristiano Oliveira",
    author_email="cristiano2132.ufv@gmail.com",  # opcional, substitua se quiser
    url="https://github.com/Cristiano2132/expdespy",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.10",
)