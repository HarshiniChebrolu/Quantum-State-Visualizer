from setuptools import setup, find_packages

setup(
    name="quantum-state-visualizer",
    version="1.0.0",
    author="Quantum Computing Research",
    description="Advanced Quantum State Visualizer with Multi-Qubit Circuit Support",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.4.0",
        "qiskit>=0.44.0",
        "qutip>=4.7.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.5.0",
        "pyqtgraph>=0.13.0",
        "pandas>=1.3.0",
        "pillow>=8.3.0",
    ],
    entry_points={
        "console_scripts": [
            "quantum-visualizer=main:main",
        ],
    },
)
