from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                             QGroupBox, QTextEdit, QFileDialog, QMessageBox)
from PyQt6.QtGui import QAction

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import your widgets and engine
from gui.bloch_widget import BlochSphereWidget
from gui.circuit_widget import CircuitWidget
from gui.controls_panel import ControlsPanel

class QuantumVisualizerMainWindow(QMainWindow):
    def __init__(self, quantum_engine):
        super().__init__()
        self.quantum_engine = quantum_engine
        self.init_ui()
        self.setup_connections()
        self.update_visualization()

    def init_ui(self):
        self.setWindowTitle("Quantum State Visualizer v1.0")
        self.setGeometry(100, 100, 1400, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left controls panel
        self.controls_panel = ControlsPanel(self.quantum_engine)
        splitter.addWidget(self.controls_panel)

        # Center panel
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)

        self.circuit_widget = CircuitWidget()
        center_layout.addWidget(self.circuit_widget)

        self.bloch_widget = BlochSphereWidget(self.quantum_engine.num_qubits)
        center_layout.addWidget(self.bloch_widget)

        splitter.addWidget(center_widget)

        # Info panel on right
        self.info_panel = self.create_info_panel()
        splitter.addWidget(self.info_panel)

        splitter.setSizes([300, 700, 300])

        self.create_menu_bar()
        self.statusBar().showMessage("Ready")

        # Create Matplotlib plots for prob and entropy
        self.create_probability_plot()
        self.create_entanglement_plot()

    def create_info_panel(self):
        info_widget = QWidget()
        layout = QVBoxLayout(info_widget)

        # Quantum State Display
        state_group = QGroupBox("Quantum State")
        state_layout = QVBoxLayout(state_group)
        self.state_display = QTextEdit()
        self.state_display.setMaximumHeight(150)
        self.state_display.setFont(QFont("Courier", 10))
        state_layout.addWidget(self.state_display)
        layout.addWidget(state_group)

        # Measurement Probabilities Display
        prob_group = QGroupBox("Measurement Probabilities")
        self.prob_group_layout = QVBoxLayout(prob_group)
        self.prob_display = QTextEdit()
        self.prob_display.setMaximumHeight(150)
        self.prob_display.setFont(QFont("Courier", 10))
        self.prob_group_layout.addWidget(self.prob_display)
        layout.addWidget(prob_group)

        # Entanglement Analysis Display
        ent_group = QGroupBox("Entanglement Analysis")
        self.ent_group_layout = QVBoxLayout(ent_group)
        self.entanglement_display = QTextEdit()
        self.entanglement_display.setMaximumHeight(100)
        self.entanglement_display.setFont(QFont("Courier", 10))
        self.ent_group_layout.addWidget(self.entanglement_display)
        layout.addWidget(ent_group)

        # Bloch Coordinates Display
        bloch_group = QGroupBox("Bloch Coordinates")
        bloch_layout = QVBoxLayout(bloch_group)
        self.bloch_coords_display = QTextEdit()
        self.bloch_coords_display.setMaximumHeight(100)
        self.bloch_coords_display.setFont(QFont("Courier", 10))
        bloch_layout.addWidget(self.bloch_coords_display)
        layout.addWidget(bloch_group)

        layout.addStretch()
        return info_widget

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        new_action = QAction('New Circuit', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_circuit)
        file_menu.addAction(new_action)

        open_action = QAction('Open QASM...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_qasm)
        file_menu.addAction(open_action)

        save_action = QAction('Save QASM...', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_qasm)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu('View')
        reset_view_action = QAction('Reset View', self)
        reset_view_action.triggered.connect(self.reset_view)
        view_menu.addAction(reset_view_action)

        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_connections(self):
        self.controls_panel.gate_applied.connect(self.on_gate_applied)
        self.controls_panel.circuit_reset.connect(self.on_circuit_reset)

    def create_probability_plot(self):
        self.prob_fig = Figure(figsize=(4, 2))
        self.prob_canvas = FigureCanvas(self.prob_fig)
        self.prob_ax = self.prob_fig.add_subplot(111)
        self.prob_group_layout.addWidget(self.prob_canvas)

    def create_entanglement_plot(self):
        self.ent_fig = Figure(figsize=(4, 1.5))
        self.ent_canvas = FigureCanvas(self.ent_fig)
        self.ent_ax = self.ent_fig.add_subplot(111)
        self.ent_group_layout.addWidget(self.ent_canvas)

    def update_visualization(self):
        try:
            bloch_vectors = self.quantum_engine.get_bloch_vectors()
            self.bloch_widget.update_bloch_vectors(bloch_vectors)

            # Measurement probabilities textual
            probabilities = self.quantum_engine.get_measurement_probabilities()
            prob_text = "Measurement Probabilities:\n"
            for state, prob in probabilities.items():
                if prob > 1e-6:
                    prob_text += f"|{state}⟩: {prob:.4f}\n"
            self.prob_display.setText(prob_text)

            # Entanglement entropy textual
            entropies = self.quantum_engine.calculate_entanglement_entropy()
            ent_text = "Single-Qubit Entropies:\n"
            for i, entropy in enumerate(entropies):
                ent_text += f"Qubit {i}: {entropy:.4f}\n"
            self.entanglement_display.setText(ent_text)

            # Quantum state vector text
            if self.quantum_engine.state_vector is not None:
                state_text = "State Vector:\n"
                for i, amp in enumerate(self.quantum_engine.state_vector):
                    basis = format(i, f'0{self.quantum_engine.num_qubits}b')
                    state_text += f"|{basis}⟩: {amp:.4f}\n"
                self.state_display.setText(state_text)

            # Bloch coordinates text
            bloch_text = "Bloch Coordinates:\n"
            for i, coords in enumerate(bloch_vectors):
                bloch_text += f"Q{i}: [{coords[0]:.3f}, {coords[1]:.3f}, {coords[2]:.3f}]\n"
            self.bloch_coords_display.setText(bloch_text)

            # Draw Measurement Probability Plot
            self.prob_ax.clear()
            states = list(probabilities.keys())
            values = list(probabilities.values())
            self.prob_ax.bar(states, values, color='skyblue')
            self.prob_ax.set_title("Measurement Probabilities")
            self.prob_ax.set_xlabel("States")
            self.prob_ax.set_ylabel("Probability")
            self.prob_ax.set_ylim(0, 1)
            self.prob_canvas.draw()

            # Draw Entanglement Entropy Plot
            self.ent_ax.clear()
            qubit_labels = [f"Qubit {i}" for i in range(len(entropies))]
            self.ent_ax.bar(qubit_labels, entropies, color='orange')
            self.ent_ax.set_title("Entanglement Entropy")
            self.ent_ax.set_ylabel("Entropy")
            self.ent_ax.set_ylim(0, 1)
            self.ent_canvas.draw()

            self.circuit_widget.update_circuit(self.quantum_engine.circuit)
            self.statusBar().showMessage("Visualization updated")

        except Exception as e:
            print(f"Visualization update error: {e}")
            self.statusBar().showMessage("Error updating visualization")

    def on_gate_applied(self):
        self.update_visualization()
        self.statusBar().showMessage("Gate applied successfully")

    def on_circuit_reset(self):
        self.update_visualization()
        self.statusBar().showMessage("Circuit reset")

    def new_circuit(self):
        self.quantum_engine.reset_circuit()
        self.update_visualization()
        self.statusBar().showMessage("New circuit created")

    def open_qasm(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open QASM File", "", "QASM Files (*.qasm);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    qasm_content = f.read()
                if self.quantum_engine.import_qasm_circuit(qasm_content):
                    self.update_visualization()
                    self.statusBar().showMessage(f"Loaded: {filename}")
                else:
                    QMessageBox.warning(self, "Error", "Failed to load QASM file")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"File error: {e}")

    def save_qasm(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save QASM File", "", "QASM Files (*.qasm);;All Files (*)")
        if filename:
            try:
                qasm_content = self.quantum_engine.export_circuit_qasm()
                with open(filename, 'w') as f:
                    f.write(qasm_content)
                self.statusBar().showMessage(f"Saved: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Save error: {e}")

    def reset_view(self):
        self.bloch_widget.reset_view()
        self.statusBar().showMessage("View reset")

    def show_about(self):
        QMessageBox.about(self, "About Quantum State Visualizer",
                          "Quantum State Visualizer v1.0\n\n"
                          "Advanced quantum circuit simulation and visualization\n"
                          "Built with PyQt6, Qiskit, and QuTiP")
