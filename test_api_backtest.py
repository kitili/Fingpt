#!/usr/bin/env python3
"""
Test API backtest functionality
"""
import requests
import json

def test_api_backtest():
    print("🧪 Testing API Backtest Functionality")
    print("=" * 50)
    
    # Test different date ranges
    test_cases = [
        {
            "name": "Recent 6 months",
            "data": {
                "symbol": "AAPL",
                "strategy": "moving_average",
                "start_date": "2024-06-01",
                "end_date": "2024-12-31",
                "initial_cash": 100000
            }
        },
        {
            "name": "Recent 3 months",
            "data": {
                "symbol": "AAPL",
                "strategy": "moving_average",
                "start_date": "2024-10-01",
                "end_date": "2024-12-31",
                "initial_cash": 100000
            }
        },
        {
            "name": "Last month",
            "data": {
                "symbol": "AAPL",
                "strategy": "moving_average",
                "start_date": "2024-12-01",
                "end_date": "2024-12-31",
                "initial_cash": 100000
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        print(f"   Date range: {test_case['data']['start_date']} to {test_case['data']['end_date']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/backtest",
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['total_trades']} trades, {result['total_return']:.4f} return")
                if result['trades']:
                    print(f"   📈 First trade: {result['trades'][0]}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_api_backtest()
