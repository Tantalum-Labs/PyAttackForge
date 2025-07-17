from setuptools import setup, find_packages

setup(
    name="pyattackforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    author="Shane S",
    description="Python wrapper for the AttackForge API",
    url="https://github.com/Tantalum-Labs/PyAttackForge",
    python_requires='>=3.7',
)
