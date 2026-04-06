from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyncbt",
    version="0.1.11",
    author="João P. M. Leroy",
    description="Non-iterative Correlation-based Tuning (NCbT) for data-driven control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(where="scr"),
    package_dir={"": "scr"},
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "scipy",
        "control",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Control Systems",
        # Não inclua classificador de licença
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
