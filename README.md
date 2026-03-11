# 🚀 Quantum State Visualizer

An interactive **quantum circuit simulator and state visualization tool** built with **PyQt6, Qiskit, and QuTiP**.  
It allows users to design quantum circuits, visualize quantum states on the **Bloch Sphere**, and analyze **entanglement and probabilities in real time**.

---

# ✨ Features

## 🎯 Interactive Quantum Circuit Design
- Build quantum circuits with a graphical interface
- Single-qubit gates:
  - X
  - Y
  - Z
  - H
  - S
  - T
- Two-qubit **CNOT gate**
- Parametric rotation gates:
  - RX
  - RY
  - RZ
- Real-time circuit diagram updates

---

## 🌐 3D Bloch Sphere Visualization
- Multiple Bloch spheres (up to **5 qubits**)
- Real-time **state vector visualization**
- Interactive **3D rotation and zoom**
- Color-coded axes
  - X → Red
  - Y → Green
  - Z → Blue
- Semi-transparent spheres with state vectors

---

## 📊 Analysis Tools
- **Measurement Probabilities**  
  Bar chart of all basis states

- **Entanglement Analysis**  
  Von Neumann entropy calculation

- **State Vector Display**  
  Full quantum state representation

- **Bloch Coordinates**  
  Real-time (x, y, z) coordinates for each qubit

---

## 🎮 Pre-built Circuit Examples
- Bell State |Φ⁺⟩
- GHZ State
- Superposition |+⟩
- Random circuit generator

---

## 💾 File Operations
- Import circuits in **OpenQASM format**
- Export circuits
- Save / load configurations
- Example circuits included

---

# 🛠 Tech Stack

### Quantum Computing
- Qiskit
- QuTiP

### GUI
- PyQt6

### Visualization
- PyQtGraph
- Matplotlib
- OpenGL

### Scientific Libraries
- NumPy

---

# 📁 Project Structure

```
quantum-state-visualizer/

src/
   core/
      quantum_engine.py

   gui/
      bloch_widget.py
      circuit_widget.py
      controls_panel.py
      main_window.py

   visualization/
      plots.py

   utils/
      helpers.py

assets/
   icons/
   demo.gif

examples/
   bell_state.qasm
   ghz_state.qasm
   superposition.qasm

tests/
   test_circuits.py

docs/
   user_guide.md

main.py
create_project.py
requirements.txt
```

---

# 🚀 Installation & Setup

## 1 Clone the Repository

```
git clone https://github.com/yourusername/quantum-state-visualizer.git
cd quantum-state-visualizer
```

---

## 2 Install Dependencies

```
pip install PyQt6 numpy matplotlib pyqtgraph qiskit qutip PyOpenGL
```

Or install using requirements file

```
pip install -r requirements.txt
```

---

## 3 Run the Application

```
python main.py
```

The GUI application will launch.

---

# 🎮 Usage Guide

## Basic Operations

### Set Number of Qubits
Use the **spinner in Circuit Settings** to select **1–5 qubits**.

### Add Single-Qubit Gates
Select target qubit and click:

```
X
Y
Z
H
S
T
```

### Add CNOT Gate

Select

```
Control Qubit
Target Qubit
```

Then click **CNOT**.

### Rotation Gates

Adjust angle slider and apply

```
RX
RY
RZ
```

### Reset Circuit

Click **Reset Circuit** to clear all gates.

---

# 🧪 Example Circuits

## Bell State |Φ⁺⟩

```
H q0
CNOT q0 q1
```

Creates entangled state:

```
(|00⟩ + |11⟩) / √2
```

---

## GHZ State

```
H q0
CNOT q0 q1
CNOT q0 q2
```

Creates state:

```
(|000⟩ + |111⟩) / √2
```

---

## Superposition |+⟩

```
H q0
```

Creates

```
(|0⟩ + |1⟩) / √2
```

---

# 📊 Visualization Features

### Bloch Sphere
- Rotate with mouse drag
- Zoom with scroll wheel

### Circuit Diagram
- Updates automatically when gates are added

### Probability Plot
Displays measurement probabilities.

### Entropy Plot
Shows entanglement between qubits.

### Info Panel
Displays:
- State vector
- Bloch coordinates
- Measurement statistics

---

# ⚙️ Technical Details

## Quantum Engine

The simulation backend uses:

- **Qiskit** for circuit simulation
- **QuTiP** for advanced quantum operations

Capabilities:

- State vector simulation
- Density matrix calculations
- Entanglement entropy
- Bloch vector extraction

---

# Supported Gates

| Gate | Type | Description |
|-----|------|-------------|
| X | Single | Pauli-X |
| Y | Single | Pauli-Y |
| Z | Single | Pauli-Z |
| H | Single | Hadamard |
| S | Single | Phase gate |
| T | Single | π/4 phase gate |
| CNOT | Two | Controlled-NOT |
| RX | Parametric | X rotation |
| RY | Parametric | Y rotation |
| RZ | Parametric | Z rotation |

---

# 📦 Requirements

```
PyQt6>=6.4.0
numpy>=1.21.0
matplotlib>=3.5.0
pyqtgraph>=0.13.0
qiskit>=0.43.0
qutip>=4.7.0
PyOpenGL>=3.1.6
```

---

# 📤 Push Project to GitHub

Initialize Git

```
git init
```

Add files

```
git add .
```

Commit

```
git commit -m "Initial commit"
```

Connect GitHub repository

```
git remote add origin https://github.com/yourusername/quantum-state-visualizer.git
```

Push code

```
git branch -M main
git push -u origin main
```

---

# 🤝 Contributing

1 Fork the repository  

2 Create feature branch

```
git checkout -b feature/new-feature
```

3 Commit changes

```
git commit -m "Add new feature"
```

4 Push branch

```
git push origin feature/new-feature
```

5 Open Pull Request

---

# 📝 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgments

- Qiskit — IBM quantum computing framework  
- QuTiP — Quantum toolbox for Python  
- PyQtGraph — High-performance visualization  
- PyQt6 — GUI framework  

---

# 🛣 Roadmap

Future improvements:

- Add more gates (Toffoli, SWAP)
- Quantum noise simulation
- Measurement simulation
- Custom gate support
- Export visualizations as images
- Quantum algorithm templates
- Real quantum hardware backend support

---

# 📧 Support

If you encounter issues:

- Open a **GitHub Issue**
- Review example circuits in `examples/`
- Check documentation in `docs/`

---

<div align="center">

🚀 Happy Quantum Computing!

</div>
