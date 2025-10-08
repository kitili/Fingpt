#!/usr/bin/env python3
"""
FinGPT API Runner
================

Script to run the FinGPT FastAPI server.
Demonstrates: API server startup, configuration, error handling
"""

import sys
import os
import uvicorn
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas',
        'numpy',
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
    """Main function to run the API server"""
    try:
        # Check dependencies
        if not check_dependencies():
            return 1
        
        logger.info("Starting FinGPT API Server...")
        logger.info("API will be available at: http://localhost:8000")
        logger.info("API documentation at: http://localhost:8000/docs")
        logger.info("Press Ctrl+C to stop the server")
        
        # Run FastAPI server
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        logger.info("API server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
