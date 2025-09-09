from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyattackforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    author="Shane S",
    description="Python wrapper for the AttackForge API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tantalum-Labs/PyAttackForge",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',
)
