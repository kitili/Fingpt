#!/usr/bin/env python3
"""
Direct test of API backtest functionality
"""
import requests
import json
import time

def test_api_direct():
    print("🧪 Direct API Backtest Test")
    print("=" * 50)
    
    # Test with a very recent date range
    test_data = {
        "symbol": "AAPL",
        "strategy": "moving_average",
        "start_date": "2024-10-01",
        "end_date": "2025-01-31",
        "initial_cash": 100000
    }
    
    print(f"Testing with date range: {test_data['start_date']} to {test_data['end_date']}")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/backtest",
            json=test_data,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Strategy: {result['strategy']}")
            print(f"   Symbol: {result['symbol']}")
            print(f"   Total trades: {result['total_trades']}")
            print(f"   Total return: {result['total_return']}")
            print(f"   Win rate: {result['win_rate']}")
            
            if result['trades']:
                print(f"   First trade: {result['trades'][0]}")
            else:
                print("   No trades executed")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_api_direct()
