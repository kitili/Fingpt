#!/usr/bin/env python3
"""
FinGPT Frontend Runner
=====================

Script to run the React frontend development server.
Demonstrates: Frontend development, React setup, development workflow
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Node.js version: {result.stdout.strip()}")
            return True
        else:
            logger.error("Node.js is not installed or not in PATH")
            return False
    except FileNotFoundError:
        logger.error("Node.js is not installed")
        return False

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"npm version: {result.stdout.strip()}")
            return True
        else:
            logger.error("npm is not installed or not in PATH")
            return False
    except FileNotFoundError:
        logger.error("npm is not installed")
        return False

def install_dependencies(frontend_dir):
    """Install frontend dependencies"""
    try:
        logger.info("Installing frontend dependencies...")
        result = subprocess.run(
            ['npm', 'install'],
            cwd=frontend_dir,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def start_frontend_server(frontend_dir):
    """Start the React development server"""
    try:
        logger.info("Starting React development server...")
        logger.info("Frontend will be available at: http://localhost:3000")
        logger.info("Press Ctrl+C to stop the server")
        
        # Start the development server
        subprocess.run(
            ['npm', 'start'],
            cwd=frontend_dir,
            check=True
        )
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start frontend server: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("Frontend server stopped by user")
        return True

def main():
    """Main function to run the frontend"""
    try:
        # Get the frontend directory
        script_dir = Path(__file__).parent
        frontend_dir = script_dir / "frontend"
        
        # Check if frontend directory exists
        if not frontend_dir.exists():
            logger.error(f"Frontend directory not found: {frontend_dir}")
            return 1
        
        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            logger.error(f"package.json not found in {frontend_dir}")
            return 1
        
        # Check Node.js and npm
        if not check_node_installed():
            logger.error("Please install Node.js from https://nodejs.org/")
            return 1
        
        if not check_npm_installed():
            logger.error("Please install npm (usually comes with Node.js)")
            return 1
        
        # Install dependencies
        if not install_dependencies(frontend_dir):
            return 1
        
        # Start the frontend server
        if not start_frontend_server(frontend_dir):
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Frontend setup stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
