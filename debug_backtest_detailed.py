#!/usr/bin/env python3
"""
Detailed debug script for backtesting functionality
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.data.collectors.market_data import MarketDataCollector
from src.analysis.trading.backtesting import Backtester, MovingAverageStrategy
import pandas as pd
from datetime import datetime

def debug_backtest_detailed():
    print("🔍 Detailed Backtesting Debug")
    print("=" * 50)
    
    # Initialize components
    collector = MarketDataCollector()
    backtester = Backtester()
    strategy = MovingAverageStrategy()
    
    # Test data fetching
    data = collector.get_stock_data("AAPL", "1y")
    start_date = pd.to_datetime("2024-06-01")
    end_date = pd.to_datetime("2024-12-31")
    
    # Convert index to datetime if needed and handle timezone
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)
    if data.index.tz is not None:
        data.index = data.index.tz_localize(None)
    
    filtered_data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    # Generate signals
    data_with_signals = strategy.generate_signals(filtered_data)
    
    print("Signal Analysis:")
    print(f"Total rows: {len(data_with_signals)}")
    print(f"Short window: {strategy.short_window}")
    print(f"Long window: {strategy.long_window}")
    
    # Show first few rows with signals
    print("\nFirst 10 rows with signals:")
    display_cols = ['Close', 'SMA_short', 'SMA_long', 'Signal', 'Position']
    print(data_with_signals[display_cols].head(10))
    
    # Show last few rows
    print("\nLast 10 rows with signals:")
    print(data_with_signals[display_cols].tail(10))
    
    # Check for position changes
    position_changes = data_with_signals[data_with_signals['Position'] != 0]
    print(f"\nPosition changes found: {len(position_changes)}")
    if len(position_changes) > 0:
        print("Position change details:")
        print(position_changes[['Close', 'SMA_short', 'SMA_long', 'Signal', 'Position']])
    
    # Test individual should_buy calls
    print("\nTesting should_buy calls:")
    for i in range(strategy.long_window, min(strategy.long_window + 10, len(data_with_signals))):
        should_buy = strategy.should_buy(data_with_signals, i)
        position = data_with_signals['Position'].iloc[i]
        print(f"Index {i}: Position={position}, Should Buy={should_buy}")

if __name__ == "__main__":
    debug_backtest_detailed()
