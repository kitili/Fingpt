#!/usr/bin/env python3
"""
Debug script for backtesting functionality
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.data.collectors.market_data import MarketDataCollector
from src.analysis.trading.backtesting import Backtester, MovingAverageStrategy
import pandas as pd
from datetime import datetime

def debug_backtest():
    print("🔍 Debugging Backtesting Functionality")
    print("=" * 50)
    
    # Initialize components
    collector = MarketDataCollector()
    backtester = Backtester()
    strategy = MovingAverageStrategy()
    
    # Test data fetching
    print("1. Testing data fetching...")
    data = collector.get_stock_data("AAPL", "1y")
    
    if data is None or data.empty:
        print("❌ No data fetched")
        return
    
    print(f"✅ Data fetched: {len(data)} rows")
    print(f"   Date range: {data.index[0]} to {data.index[-1]}")
    print(f"   Columns: {list(data.columns)}")
    
    # Test date filtering
    print("\n2. Testing date filtering...")
    start_date = pd.to_datetime("2024-06-01")
    end_date = pd.to_datetime("2024-12-31")
    
    # Convert index to datetime if needed and handle timezone
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)
    
    filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
    print(f"✅ Filtered data: {len(filtered_data)} rows")
    
    if filtered_data.empty:
        print("❌ No data in date range")
        return
    
    # Test strategy signal generation
    print("\n3. Testing strategy signal generation...")
    data_with_signals = strategy.generate_signals(filtered_data)
    print(f"✅ Signals generated: {len(data_with_signals)} rows")
    
    # Check for signals
    if 'Signal' in data_with_signals.columns:
        signal_counts = data_with_signals['Signal'].value_counts()
        print(f"   Signal distribution: {dict(signal_counts)}")
        
        # Check for position changes
        if 'Position' in data_with_signals.columns:
            position_changes = data_with_signals['Position'].value_counts()
            print(f"   Position changes: {dict(position_changes)}")
    
    # Test backtest execution
    print("\n4. Testing backtest execution...")
    try:
        result = backtester.run_backtest(strategy, filtered_data, "AAPL")
        print(f"✅ Backtest completed")
        print(f"   Total trades: {result.total_trades}")
        print(f"   Total return: {result.total_return:.4f}")
        print(f"   Win rate: {result.win_rate:.4f}")
        
        if result.trades:
            print(f"   First trade: {result.trades[0]}")
        else:
            print("   No trades executed")
            
    except Exception as e:
        print(f"❌ Backtest failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_backtest()
