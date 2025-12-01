#!/usr/bin/env python3
"""
Main entry point for the E-commerce AI Support System.

This script launches the Streamlit web interface for the customer support chat system.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Streamlit application."""
    # Get the path to the customer chat UI
    ui_path = Path(__file__).parent / "src" / "ui" / "customer_chat.py"
    
    if not ui_path.exists():
        print(f"Error: UI file not found at {ui_path}")
        sys.exit(1)
    
    print("🚀 Starting E-commerce AI Support System...")
    print("📱 Opening web interface at http://localhost:8501")
    print("🔄 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(ui_path),
            "--server.headless", "true",
            "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 