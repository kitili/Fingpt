#!/usr/bin/env python3
"""
FinGPT Dashboard Runner
======================

Script to run the FinGPT Streamlit dashboard.
Demonstrates: Application entry point, configuration, error handling
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'yfinance',
        'scikit-learn',
        'cvxpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.info("Install missing packages with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function to run the dashboard"""
    try:
        # Get the directory containing this script
        script_dir = Path(__file__).parent
        dashboard_path = script_dir / "web" / "dashboard" / "main.py"
        
        # Check if dashboard file exists
        if not dashboard_path.exists():
            logger.error(f"Dashboard file not found: {dashboard_path}")
            return 1
        
        # Check dependencies
        if not check_dependencies():
            return 1
        
        logger.info("Starting FinGPT Dashboard...")
        logger.info("Dashboard will be available at: http://localhost:8501")
        logger.info("Press Ctrl+C to stop the dashboard")
        
        # Run Streamlit dashboard
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        logger.info("Dashboard stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running dashboard: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
