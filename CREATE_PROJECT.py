#!/usr/bin/env python3
"""
Quantum State Visualizer - Project Setup Script
Run this script to create the complete project structure
"""

import os
from pathlib import Path

def create_project_structure():
    """Create the complete project directory structure"""
    
    # Define directory structure
    directories = [
        'src',
        'src/core',
        'src/gui',
        'src/visualization',
        'src/utils',
        'assets',
        'assets/icons',
        'examples',
        'tests',
        'docs'
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py files for Python packages
        if directory.startswith('src'):
            init_file = Path(directory) / '__init__.py'
            if not init_file.exists():
                init_file.write_text('# -*- coding: utf-8 -*-\n')
    
    print("✓ Project directory structure created")
    
    # Create example QASM files
    create_example_files()
    
    print("✓ Example files created")
    print("\n🎉 Project setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python main.py")

def create_example_files():
    """Create example QASM circuit files"""
    
    examples_dir = Path('examples')
    
    # Bell state circuit
    bell_qasm = """OPENQASM 2.0;
include \"qelib1.inc\";

qreg q[2];
creg c[1];

h q;
cx q, q[2];

measure q -> c;
"""
    
    (examples_dir / 'bell_state.qasm').write_text(bell_qasm)
    
    # GHZ state circuit
    ghz_qasm = """OPENQASM 2.0;
include \"qelib1.inc\";

qreg q[3];
creg c[3];

h q;
cx q, q[2];
cx q, q[1];

measure q -> c;
"""
    
    (examples_dir / 'ghz_state.qasm').write_text(ghz_qasm)
    
    # Superposition circuit
    superposition_qasm = """OPENQASM 2.0;
include \"qelib1.inc\";

qreg q[2];
creg c[2];

h q;

measure q -> c;
"""
    
    (examples_dir / 'superposition.qasm').write_text(superposition_qasm)

if __name__ == "__main__":
    create_project_structure()
