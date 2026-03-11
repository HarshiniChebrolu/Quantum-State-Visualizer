"""
Controls Panel for Gate Application and Circuit Management
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QComboBox, QSpinBox, QGroupBox,
                           QGridLayout, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal
import numpy as np


class ControlsPanel(QWidget):
    gate_applied = pyqtSignal()
    circuit_reset = pyqtSignal()
    
    def __init__(self, quantum_engine):
        super().__init__()
        self.quantum_engine = quantum_engine
        
        # Initialize attributes here to avoid 'no attribute' errors
        self.control_selector = None
        self.target_selector = None
        self.single_qubit_selector = None
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Quantum Controls")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        circuit_group = self.create_circuit_settings()
        layout.addWidget(circuit_group)
        
        single_gates = self.create_single_qubit_gates()
        layout.addWidget(single_gates)
        
        two_gates = self.create_two_qubit_gates()
        layout.addWidget(two_gates)
        
        param_gates = self.create_parametric_gates()
        layout.addWidget(param_gates)
        
        management = self.create_circuit_management()
        layout.addWidget(management)
        
        examples = self.create_example_circuits()
        layout.addWidget(examples)
        
        layout.addStretch()
        
    def create_circuit_settings(self):
        group = QGroupBox("Circuit Settings")
        layout = QGridLayout(group)
        
        layout.addWidget(QLabel("Qubits:"), 0, 0)
        self.qubit_spinner = QSpinBox()
        self.qubit_spinner.setRange(1, 5)
        self.qubit_spinner.setValue(self.quantum_engine.num_qubits)
        self.qubit_spinner.valueChanged.connect(self.on_qubit_count_changed)
        layout.addWidget(self.qubit_spinner, 0, 1)
        
        return group
    
    def create_single_qubit_gates(self):
        group = QGroupBox("Single-Qubit Gates")
        layout = QGridLayout(group)
        
        layout.addWidget(QLabel("Target Qubit:"), 0, 0)
        self.single_qubit_selector = QComboBox()
        self.update_qubit_selectors()
        layout.addWidget(self.single_qubit_selector, 0, 1)
        
        gates = [('X', 'Pauli-X'), ('Y', 'Pauli-Y'), ('Z', 'Pauli-Z'), 
                ('H', 'Hadamard'), ('S', 'Phase'), ('T', 'T-gate')]
        
        row, col = 1, 0
        for gate_name, tooltip in gates:
            btn = QPushButton(gate_name)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, g=gate_name: self.apply_single_gate(g))
            layout.addWidget(btn, row, col)
            
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        return group
    
    def create_two_qubit_gates(self):
        group = QGroupBox("Two-Qubit Gates")
        layout = QGridLayout(group)
        
        layout.addWidget(QLabel("Control:"), 0, 0)
        self.control_selector = QComboBox()
        layout.addWidget(self.control_selector, 0, 1)
        
        layout.addWidget(QLabel("Target:"), 1, 0)
        self.target_selector = QComboBox()
        layout.addWidget(self.target_selector, 1, 1)
        
        cnot_btn = QPushButton("CNOT")
        cnot_btn.setToolTip("Controlled-NOT gate")
        cnot_btn.clicked.connect(self.apply_cnot_gate)
        layout.addWidget(cnot_btn, 2, 0, 1, 2)
        
        self.update_qubit_selectors()
        
        return group
    
    def create_parametric_gates(self):
        group = QGroupBox("Parametric Gates")
        layout = QGridLayout(group)
        
        layout.addWidget(QLabel("Angle (π):"), 0, 0)
        self.angle_slider = QSlider(Qt.Orientation.Horizontal)
        self.angle_slider.setRange(-200, 200)
        self.angle_slider.setValue(50)
        self.angle_slider.valueChanged.connect(self.update_angle_display)
        layout.addWidget(self.angle_slider, 0, 1)
        
        self.angle_display = QLabel("π/2")
        layout.addWidget(self.angle_display, 0, 2)
        
        rx_btn = QPushButton("RX")
        rx_btn.setToolTip("X-rotation gate")
        rx_btn.clicked.connect(lambda: self.apply_rotation_gate('RX'))
        layout.addWidget(rx_btn, 1, 0)
        
        ry_btn = QPushButton("RY")
        ry_btn.setToolTip("Y-rotation gate")
        ry_btn.clicked.connect(lambda: self.apply_rotation_gate('RY'))
        layout.addWidget(ry_btn, 1, 1)
        
        rz_btn = QPushButton("RZ")
        rz_btn.setToolTip("Z-rotation gate")
        rz_btn.clicked.connect(lambda: self.apply_rotation_gate('RZ'))
        layout.addWidget(rz_btn, 1, 2)
        
        return group
    
    def create_circuit_management(self):
        group = QGroupBox("Circuit Management")
        layout = QVBoxLayout(group)
        
        reset_btn = QPushButton("Reset Circuit")
        reset_btn.clicked.connect(self.reset_circuit)
        layout.addWidget(reset_btn)
        
        random_btn = QPushButton("Generate Random Circuit")
        random_btn.clicked.connect(self.generate_random_circuit)
        layout.addWidget(random_btn)
        
        return group
    
    def create_example_circuits(self):
        group = QGroupBox("Example Circuits")
        layout = QVBoxLayout(group)
        
        bell_btn = QPushButton("Bell State |Φ+⟩")
        bell_btn.clicked.connect(self.create_bell_state)
        layout.addWidget(bell_btn)
        
        ghz_btn = QPushButton("GHZ State")
        ghz_btn.clicked.connect(self.create_ghz_state)
        layout.addWidget(ghz_btn)
        
        super_btn = QPushButton("Superposition |+⟩")
        super_btn.clicked.connect(self.create_superposition)
        layout.addWidget(super_btn)
        
        return group
    
    def update_qubit_selectors(self):
        num_qubits = self.quantum_engine.num_qubits
        
        if self.single_qubit_selector is not None:
            self.single_qubit_selector.clear()
            for i in range(num_qubits):
                self.single_qubit_selector.addItem(f"Qubit {i}")
        
        if self.control_selector is not None:
            self.control_selector.clear()
        if self.target_selector is not None:
            self.target_selector.clear()
        for i in range(num_qubits):
            if self.control_selector is not None:
                self.control_selector.addItem(f"Qubit {i}")
            if self.target_selector is not None:
                self.target_selector.addItem(f"Qubit {i}")
        
        if self.target_selector is not None and num_qubits > 1:
            self.target_selector.setCurrentIndex(1)
    
    def on_qubit_count_changed(self, value):
        self.quantum_engine.reset_circuit(value)
        self.update_qubit_selectors()
        self.circuit_reset.emit()
    
    def apply_single_gate(self, gate_name):
        qubit = self.single_qubit_selector.currentIndex()
        if self.quantum_engine.add_gate(gate_name, [qubit]):
            self.gate_applied.emit()
    
    def apply_cnot_gate(self):
        control = self.control_selector.currentIndex()
        target = self.target_selector.currentIndex()
        
        if control != target:
            if self.quantum_engine.add_gate('CNOT', [control, target]):
                self.gate_applied.emit()
    
    def apply_rotation_gate(self, gate_name):
        qubit = self.single_qubit_selector.currentIndex()
        angle = (self.angle_slider.value() / 100.0) * np.pi
        
        if self.quantum_engine.add_gate(gate_name, [qubit], angle=angle):
            self.gate_applied.emit()
    
    def update_angle_display(self, value):
        angle_fraction = value / 100.0
        if abs(angle_fraction) < 0.01:
            self.angle_display.setText("0")
        elif abs(abs(angle_fraction) - 0.5) < 0.01:
            sign = "+" if angle_fraction > 0 else "-"
            self.angle_display.setText(f"{sign}π/2")
        elif abs(abs(angle_fraction) - 1) < 0.01:
            sign = "+" if angle_fraction > 0 else "-"
            self.angle_display.setText(f"{sign}π")
        else:
            self.angle_display.setText(f"{angle_fraction:.2f}π")
    
    def reset_circuit(self):
        self.quantum_engine.reset_circuit()
        self.circuit_reset.emit()
    
    def generate_random_circuit(self):
        import random
        self.quantum_engine.reset_circuit()
        
        num_gates = random.randint(5, 10)
        gates = ['H', 'X', 'Y', 'Z', 'S', 'T']
        
        for _ in range(num_gates):
            gate = random.choice(gates)
            qubit = random.randint(0, self.quantum_engine.num_qubits - 1)
            self.quantum_engine.add_gate(gate, [qubit])
            
            if self.quantum_engine.num_qubits > 1 and random.random() < 0.3:
                qubits = random.sample(range(self.quantum_engine.num_qubits), 2)
                self.quantum_engine.add_gate('CNOT', qubits)
        
        self.gate_applied.emit()
    
    def create_bell_state(self):
        if self.quantum_engine.num_qubits >= 2:
            self.quantum_engine.reset_circuit()
            self.quantum_engine.add_gate('H', [0])
            self.quantum_engine.add_gate('CNOT', [0, 1])
            self.gate_applied.emit()
    
    def create_ghz_state(self):
        if self.quantum_engine.num_qubits >= 3:
            self.quantum_engine.reset_circuit()
            self.quantum_engine.add_gate('H', [0])
            for i in range(1, min(3, self.quantum_engine.num_qubits)):
                self.quantum_engine.add_gate('CNOT', [0, i])
            self.gate_applied.emit()
    
    def create_superposition(self):
        self.quantum_engine.reset_circuit()
        self.quantum_engine.add_gate('H', [0])
        self.gate_applied.emit()
