#!/usr/bin/env python3
"""
Test script to verify frontend functionality
"""
import requests
import json
import time

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing API Endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
        else:
            print(f"❌ Health endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint: {e}")
    
    # Test portfolio optimization
    try:
        data = {
            "symbols": ["AAPL", "GOOGL"],
            "method": "risk_parity",
            "period": "1y"
        }
        response = requests.post(f"{base_url}/api/portfolio/optimize", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Portfolio optimization: {result.get('method', 'Unknown method')}")
        else:
            print(f"❌ Portfolio optimization: {response.status_code}")
    except Exception as e:
        print(f"❌ Portfolio optimization: {e}")
    
    # Test market data
    try:
        data = {
            "symbols": ["AAPL"],
            "period": "1y"
        }
        response = requests.post(f"{base_url}/api/market-data", 
                               json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Market data: OK")
            else:
                print(f"❌ Market data: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Market data: {response.status_code}")
    except Exception as e:
        print(f"❌ Market data: {e}")

def test_frontend():
    """Test frontend accessibility"""
    print("\n🌐 Testing Frontend...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Accessible")
            
            # Check if it's a React app
            if "react" in response.text.lower() or "root" in response.text:
                print("✅ Frontend: React app detected")
            else:
                print("⚠️ Frontend: May not be React app")
        else:
            print(f"❌ Frontend: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: {e}")

def test_navigation_routes():
    """Test if all navigation routes are accessible"""
    print("\n🧭 Testing Navigation Routes...")
    
    routes = [
        "/",
        "/market", 
        "/portfolio",
        "/sentiment",
        "/technical",
        "/risk",
        "/backtesting",
        "/about"
    ]
    
    for route in routes:
        try:
            response = requests.get(f"http://localhost:3000{route}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Route {route}: OK")
            else:
                print(f"❌ Route {route}: {response.status_code}")
        except Exception as e:
            print(f"❌ Route {route}: {e}")

if __name__ == "__main__":
    print("🚀 FinGPT Frontend Test Suite")
    print("=" * 50)
    
    test_api_endpoints()
    test_frontend()
    test_navigation_routes()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\n📋 Summary:")
    print("- API Server: http://localhost:8000")
    print("- Frontend: http://localhost:3000")
    print("- All navigation items should be working")
    print("- Check browser console for any JavaScript errors")
