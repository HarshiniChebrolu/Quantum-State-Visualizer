#!/usr/bin/env python3
"""
Quantum State Visualizer - Main Application Entry Point
A comprehensive desktop application for visualizing quantum states and circuits.
"""

import sys
import logging
from pathlib import Path

# Add src directory to path for absolute imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
except ImportError:
    print("PyQt6 not found. Please install it using: pip install PyQt6")
    sys.exit(1)

try:
    import qiskit
    import qutip
    import numpy as np
    import pyqtgraph as pg
except ImportError as e:
    print(f"Required quantum computing library not found: {e}")
    print("Please install required packages using: pip install -r requirements.txt")
    sys.exit(1)

# Import main window and quantum engine from your src folder
from src.gui.main_window import QuantumVisualizerMainWindow
from src.core.quantum_engine import QuantumStateEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quantum_visualizer.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger.info("Starting Quantum State Visualizer")

    # Enable High DPI scaling in PyQt6
    try:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        logger.warning("High DPI scaling attributes not available in this PyQt6 version")

    app = QApplication(sys.argv)
    app.setApplicationName("Quantum State Visualizer")
    app.setApplicationVersion("1.0.0")
    app.setStyle('Fusion')

    try:
        quantum_engine = QuantumStateEngine()
        main_window = QuantumVisualizerMainWindow(quantum_engine)
        main_window.show()
        logger.info("Application initialized successfully")

        # Run the application event loop
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application error: {e}")
        QMessageBox.critical(None, "Application Error", str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
