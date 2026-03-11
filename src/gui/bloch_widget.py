"""
3D Bloch Sphere Visualization Widget
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import pyqtgraph.opengl as gl
import numpy as np

class BlochSphereWidget(QWidget):
    """Widget for displaying multiple Bloch spheres"""

    def __init__(self, num_qubits=2):
        super().__init__()
        self.num_qubits = num_qubits
        self.bloch_vectors = [[0, 0, 1]] * num_qubits  # Initialize to |0⟩ state
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Bloch Sphere Visualization")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        # Create OpenGL widget for 3D visualization
        self.gl_widget = gl.GLViewWidget()
        self.gl_widget.setMinimumHeight(400)
        layout.addWidget(self.gl_widget)

        # Setup 3D scene
        self.setup_bloch_spheres()

    def clear_bloch_spheres(self):
        """Remove all spheres, vectors, and axes from the OpenGL widget."""
        for item in self.sphere_items + self.vector_items + self.axis_items:
            self.gl_widget.removeItem(item)
        self.sphere_items = []
        self.vector_items = []
        self.axis_items = []

    def set_num_qubits(self, new_num_qubits):
        """Change the number of displayed Bloch spheres."""
        self.num_qubits = new_num_qubits
        self.bloch_vectors = [[0, 0, 1]] * self.num_qubits
        self.clear_bloch_spheres()
        self.setup_bloch_spheres()

    def setup_bloch_spheres(self):
        """Setup 3D Bloch spheres"""
        self.sphere_items = []
        self.vector_items = []
        self.axis_items = []
        
        positions = self.calculate_sphere_positions()

        for i in range(self.num_qubits):
            pos = positions[i]

            # Create sphere
            sphere = self.create_sphere_mesh()
            sphere.translate(pos[0], pos[1], pos[2])
            sphere.setColor((0.3, 0.3, 0.8, 0.6))  # Semi-transparent blue
            self.gl_widget.addItem(sphere)
            self.sphere_items.append(sphere)

            # Create coordinate axes
            axes = self.create_coordinate_axes()
            for axis in axes:
                axis.translate(pos[0], pos[1], pos[2])
                self.gl_widget.addItem(axis)
            self.axis_items.extend(axes)

            # Create state vector
            vector = self.create_state_vector([0, 0, 1])  # |0⟩ state
            vector.translate(pos[0], pos[1], pos[2])
            self.gl_widget.addItem(vector)
            self.vector_items.append(vector)

            # Add qubit label
            self.add_text_label(f"Qubit {i}", [pos[0], pos[1], pos[2] + 1.5])
        
        # Set camera position
        self.gl_widget.setCameraPosition(distance=8, elevation=20, azimuth=45)

    def calculate_sphere_positions(self):
        """Calculate positions for multiple Bloch spheres"""
        positions = []
        if self.num_qubits == 1:
            positions = [[0, 0, 0]]
        elif self.num_qubits == 2:
            positions = [[-2, 0, 0], [2, 0, 0]]
        elif self.num_qubits == 3:
            positions = [[-3, 0, 0], [0, 0, 0], [3, 0, 0]]
        elif self.num_qubits == 4:
            positions = [[-3, -1.5, 0], [-1, -1.5, 0], [1, 1.5, 0], [3, 1.5, 0]]
        else:  # 5 or more qubits
            angle_step = 2 * np.pi / self.num_qubits
            radius = 3
            for i in range(self.num_qubits):
                angle = i * angle_step
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions.append([x, y, 0])
        return positions

    def create_sphere_mesh(self):
        """Create a 3D sphere mesh"""
        md = gl.MeshData.sphere(rows=20, cols=40, radius=1.0)
        mesh = gl.GLMeshItem(meshdata=md, smooth=True, drawFaces=True, drawEdges=False)
        return mesh

    def create_coordinate_axes(self):
        """Create X, Y, Z coordinate axes"""
        axes = []

        x_axis = gl.GLLinePlotItem(
            pos=np.array([[-1.2, 0, 0], [1.2, 0, 0]]),
            color=(1, 0, 0, 0.8), width=2
        )
        axes.append(x_axis)

        y_axis = gl.GLLinePlotItem(
            pos=np.array([[0, -1.2, 0], [0, 1.2, 0]]),
            color=(0, 1, 0, 0.8), width=2
        )
        axes.append(y_axis)

        z_axis = gl.GLLinePlotItem(
            pos=np.array([[0, 0, -1.2], [0, 0, 1.2]]),
            color=(0, 0, 1, 0.8), width=2
        )
        axes.append(z_axis)

        return axes

    def create_state_vector(self, bloch_coords):
        """Create state vector arrow"""
        x, y, z = bloch_coords
        vector_data = np.array([[0, 0, 0], [x, y, z]])
        vector = gl.GLLinePlotItem(
            pos=vector_data,
            color=(1, 1, 0, 1),  # Yellow
            width=4
        )
        return vector

    def add_text_label(self, text, position):
        """Add text label at position - placeholder"""
        # PyQtGraph's 3D widget does not support text natively
        pass

    def update_bloch_vectors(self, bloch_vectors):
        """Update Bloch vector displays"""
        self.bloch_vectors = bloch_vectors
        positions = self.calculate_sphere_positions()
        for i, coords in enumerate(bloch_vectors):
            if i < len(self.vector_items):
                self.gl_widget.removeItem(self.vector_items[i])
                pos = positions[i]
                new_vector = self.create_state_vector(coords)
                new_vector.translate(pos[0], pos[1], pos[2])
                self.gl_widget.addItem(new_vector)
                self.vector_items[i] = new_vector

    def reset_view(self):
        """Reset camera view"""
        self.gl_widget.setCameraPosition(distance=8, elevation=20, azimuth=45)
