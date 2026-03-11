"""
Quantum Circuit Visualization Widget
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches


class CircuitWidget(QWidget):
    """Widget for displaying quantum circuit diagrams"""
    
    def __init__(self):
        super().__init__()
        self.circuit = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        title = QLabel("Quantum Circuit")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title)
        
        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(200)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.canvas)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        self.draw_empty_circuit()
        
    def draw_empty_circuit(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        num_qubits = 2  # Default
        for i in range(num_qubits):
            ax.axhline(y=i, xmin=0.1, xmax=0.9, color='black', linewidth=2)
            ax.text(0.05, i, f'|q{i}⟩', fontsize=12, va='center')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.5, num_qubits - 0.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Quantum Circuit Diagram')
        
        self.canvas.draw()
        
    def update_circuit(self, circuit):
        if circuit is None:
            self.draw_empty_circuit()
            return
        
        self.circuit = circuit
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        num_qubits = circuit.num_qubits
        num_gates = len(circuit.data) if circuit.data else 0
        
        # Draw lines and labels for each qubit
        for i in range(num_qubits):
            ax.axhline(y=i, xmin=0, xmax=num_gates + 1, color='black', linewidth=2)
            ax.text(-0.5, i, f'|q{i}⟩', fontsize=12, va='center')
        
        gate_positions = {q: 0 for q in range(num_qubits)}
        
        if circuit.data:
            for gate_idx, instruction in enumerate(circuit.data):
                gate = instruction.operation
                qubits = [circuit.find_bit(qubit).index for qubit in instruction.qubits]
                
                max_pos = max(gate_positions[q] for q in qubits)
                gate_x = max_pos + 1
                
                for q in qubits:
                    gate_positions[q] = gate_x
                
                if gate.name in ['x', 'y', 'z', 'h', 's', 't']:
                    self.draw_single_qubit_gate(ax, gate.name.upper(), gate_x, qubits[0])
                elif gate.name == 'cx':
                    self.draw_cnot_gate(ax, gate_x, qubits[0], qubits[1])
                elif gate.name in ['rx', 'ry', 'rz']:
                    # Format angle nicely if available
                    angle = 0
                    if hasattr(gate, 'params') and gate.params:
                        # Handle different parameter formats
                        if isinstance(gate.params, (list, tuple)) and gate.params:
                            angle = gate.params[0]
                        elif hasattr(gate.params, '__float__'):
                            angle = float(gate.params)
                    label = f"{gate.name.upper()}({angle:.2f})"
                    self.draw_single_qubit_gate(ax, label, gate_x, qubits[0])
                else:
                    # Unknown gate - display name simply
                    self.draw_single_qubit_gate(ax, gate.name.upper(), gate_x, qubits[0])
        
        # Adjust plot limits dynamically based on gates
        max_x = max(gate_positions.values()) if gate_positions else 1
        ax.set_xlim(-1, max_x + 2)
        ax.set_ylim(-0.5, num_qubits - 0.5)
        ax.invert_yaxis()
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Quantum Circuit Diagram')
        
        self.figure.tight_layout()
        self.canvas.draw()
        
    def draw_single_qubit_gate(self, ax, gate_name, x, y):
        box = patches.Rectangle((x-0.3, y-0.3), 0.6, 0.6, 
                               linewidth=2, edgecolor='black', 
                               facecolor='lightblue')
        ax.add_patch(box)
        ax.text(x, y, gate_name, fontsize=10, ha='center', va='center', weight='bold')
    
    def draw_cnot_gate(self, ax, x, control, target):
        control_circle = patches.Circle((x, control), 0.1, facecolor='black', edgecolor='black')
        ax.add_patch(control_circle)
        
        target_circle = patches.Circle((x, target), 0.2, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(target_circle)
        
        # Vertical line connection
        y_min, y_max = min(control, target), max(control, target)
        ax.plot([x, x], [y_min, y_max], 'k-', linewidth=2)
        
        # Horizontal line for target plus cross
        ax.plot([x-0.15, x+0.15], [target, target], 'k-', linewidth=2)
        ax.plot([x, x], [target-0.15, target+0.15], 'k-', linewidth=2)