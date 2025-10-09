#!/usr/bin/env python3
"""
Test script to verify navigation functionality
"""
import requests
import time

def test_simple_navigation():
    """Test navigation using simple HTTP requests"""
    print("\n🌐 Testing Simple Navigation...")
    
    # Test if the main page loads
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Main page: Accessible")
            
            # Check if it contains React app elements
            if "root" in response.text and "react" in response.text.lower():
                print("✅ Main page: React app detected")
                return True
            else:
                print("❌ Main page: Not a React app")
                return False
        else:
            print(f"❌ Main page: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page: {e}")
        return False

if __name__ == "__main__":
    print("🚀 FinGPT Navigation Test Suite")
    print("=" * 50)
    
    # Test simple navigation first
    simple_test = test_simple_navigation()
    
    if simple_test:
        print("\n✅ Basic navigation test passed!")
        print("\n📋 Summary:")
        print("- Frontend is accessible at http://localhost:3000")
        print("- React app is properly loaded")
        print("- Navigation should work in the browser")
        print("\n💡 Note: Direct HTTP requests to specific routes may not work")
        print("   due to client-side routing. Use the browser to test navigation.")
    else:
        print("\n❌ Basic navigation test failed!")
    
    print("\n" + "=" * 50)
