"""
Quantum State Engine - Core quantum computing functionality
"""

import numpy as np
from typing import List, Union
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace

class QuantumStateEngine:
    """Advanced quantum state simulation and analysis engine"""
    
    def __init__(self, num_qubits: int = 2):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits)
        self.state_vector = None
        self.density_matrix = None
        self.simulator = AerSimulator()
        
    def reset_circuit(self, num_qubits: int = None):
        """Reset quantum circuit to initial state"""
        if num_qubits:
            self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(self.num_qubits)
        self.state_vector = None
        self.density_matrix = None
    
    def add_gate(self, gate_name: str, qubit_indices: List[int], **params):
        """Add quantum gate to circuit"""
        try:
            if gate_name.upper() == 'H':
                self.circuit.h(qubit_indices[0])
            elif gate_name.upper() == 'X':
                self.circuit.x(qubit_indices[0])
            elif gate_name.upper() == 'Y':
                self.circuit.y(qubit_indices[0])
            elif gate_name.upper() == 'Z':
                self.circuit.z(qubit_indices[0])
            elif gate_name.upper() == 'CNOT':
                self.circuit.cx(qubit_indices[0], qubit_indices[1])
            elif gate_name.upper() == 'S':
                self.circuit.s(qubit_indices[0])
            elif gate_name.upper() == 'T':
                self.circuit.t(qubit_indices[0])
            elif gate_name.upper() == 'RX':
                angle = params.get('angle', np.pi/2)
                self.circuit.rx(angle, qubit_indices[0])
            elif gate_name.upper() == 'RY':
                angle = params.get('angle', np.pi/2)
                self.circuit.ry(angle, qubit_indices[0])
            elif gate_name.upper() == 'RZ':
                angle = params.get('angle', np.pi/2)
                self.circuit.rz(angle, qubit_indices[0])
            else:
                print(f"Gate {gate_name} not recognized or not implemented.")
                return False
                
            # Update state after adding gate
            self.simulate_circuit()
            return True
            
        except Exception as e:
            print(f"Error adding gate {gate_name}: {e}")
            return False
    
    def simulate_circuit(self):
        """Simulate current quantum circuit"""
        try:
            # Use Statevector for simulation instead of the old execute method
            self.state_vector = Statevector.from_instruction(self.circuit)
            self.density_matrix = DensityMatrix(self.state_vector)
            return True
        except Exception as e:
            print(f"Simulation error: {e}")
            return False
    
    def get_reduced_density_matrices(self):
        """Get single-qubit reduced density matrices"""
        if self.density_matrix is None:
            if not self.simulate_circuit():
                return []
        
        reduced_states = []
        for i in range(self.num_qubits):
            trace_qubits = [j for j in range(self.num_qubits) if j != i]
            
            if trace_qubits:
                reduced_dm = partial_trace(self.density_matrix, trace_qubits)
            else:
                reduced_dm = self.density_matrix
                
            reduced_states.append(reduced_dm.data)
        
        return reduced_states
    
    def get_bloch_vectors(self):
        """Convert reduced density matrices to Bloch vectors"""
        reduced_states = self.get_reduced_density_matrices()
        bloch_vectors = []
        
        for dm in reduced_states:
            x = 2 * np.real(dm[0, 1])
            y = 2 * np.imag(dm[1, 0])
            z = np.real(dm[0, 0] - dm[1, 1])
            bloch_vectors.append([x, y, z])
        
        return bloch_vectors
    
    def get_measurement_probabilities(self):
        """Get computational basis measurement probabilities"""
        if self.state_vector is None:
            if not self.simulate_circuit():
                return {}
        
        probabilities = np.abs(self.state_vector) ** 2
        basis_states = [format(i, f'0{self.num_qubits}b') for i in range(len(probabilities))]
        
        return dict(zip(basis_states, probabilities))
    
    def calculate_entanglement_entropy(self):
        """Calculate entanglement entropy for each qubit"""
        reduced_states = self.get_reduced_density_matrices()
        if not reduced_states:
            return []
            
        entropies = []
        
        for dm in reduced_states:
            eigenvals = np.linalg.eigvals(dm)
            eigenvals = eigenvals[eigenvals > 1e-12]
            entropy = -np.sum(eigenvals * np.log2(eigenvals)) if len(eigenvals) > 0 else 0
            entropies.append(np.real(entropy))
        
        return entropies
    
    def export_circuit_qasm(self):
        """Export circuit as OpenQASM string"""
        return self.circuit.qasm()
    
    def import_qasm_circuit(self, qasm_string: str):
        """Import circuit from OpenQASM string"""
        try:
            self.circuit = QuantumCircuit.from_qasm_str(qasm_string)
            self.num_qubits = self.circuit.num_qubits
            self.simulate_circuit()
            return True
        except Exception as e:
            print(f"QASM import error: {e}")
            return False


# Example usage and test function
def test_quantum_engine():
    """Test function to demonstrate the quantum engine"""
    engine = QuantumStateEngine(2)
    
    # Add some gates
    engine.add_gate('H', [0])
    engine.add_gate('CNOT', [0, 1])
    
    # Get results
    print("State vector:", engine.state_vector)
    print("Bloch vectors:", engine.get_bloch_vectors())
    print("Measurement probabilities:", engine.get_measurement_probabilities())
    print("Entanglement entropy:", engine.calculate_entanglement_entropy())
    
    # Export to QASM
    qasm_str = engine.export_circuit_qasm()
    print("QASM representation:")
    print(qasm_str)

if __name__ == "__main__":
    test_quantum_engine()