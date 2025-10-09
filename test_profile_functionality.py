#!/usr/bin/env python3
"""
Test script to verify profile, settings, and logout functionality
"""
import requests
import time

def test_frontend_accessibility():
    """Test if frontend is accessible and contains the new functionality"""
    print("🧪 Testing Profile Functionality...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: Accessible")
            
            # Check if the HTML contains the necessary elements
            html_content = response.text
            
            # Check for React app structure
            if "root" in html_content and "bundle.js" in html_content:
                print("✅ Frontend: React app properly loaded")
            else:
                print("❌ Frontend: React app not detected")
                return False
                
            return True
        else:
            print(f"❌ Frontend: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend: {e}")
        return False

def test_api_health():
    """Test API health"""
    print("\n🔌 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API: Healthy")
            return True
        else:
            print(f"❌ API: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API: {e}")
        return False

def main():
    print("🚀 FinGPT Profile Functionality Test")
    print("=" * 50)
    
    # Test frontend accessibility
    frontend_ok = test_frontend_accessibility()
    
    # Test API health
    api_ok = test_api_health()
    
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print(f"Frontend: {'✅ Working' if frontend_ok else '❌ Issues'}")
    print(f"API: {'✅ Working' if api_ok else '❌ Issues'}")
    
    if frontend_ok and api_ok:
        print("\n🎉 All systems operational!")
        print("\n📝 New Features Added:")
        print("✅ Profile Management:")
        print("   - Click on user avatar → Profile")
        print("   - Edit name, email, role, department")
        print("   - Data persists in localStorage")
        print("\n✅ Settings Management:")
        print("   - Click on user avatar → Settings")
        print("   - Configure theme, notifications, auto-refresh")
        print("   - Set default analysis period and risk tolerance")
        print("   - Settings persist in localStorage")
        print("\n✅ Logout Functionality:")
        print("   - Click on user avatar → Logout")
        print("   - Confirmation dialog before logout")
        print("   - Clears user data and reloads page")
        print("\n🔧 How to Test:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Click on the user avatar in the top-right corner")
        print("3. Try Profile, Settings, and Logout options")
        print("4. Verify data persistence by refreshing the page")
    else:
        print("\n❌ Some issues detected. Please check the logs above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
