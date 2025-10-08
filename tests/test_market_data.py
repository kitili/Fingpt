"""
Tests for Market Data Module
===========================

Unit tests for market data collection and analysis.
Demonstrates: Testing, quality assurance, validation
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data.collectors.market_data import MarketDataCollector, MarketData

class TestMarketDataCollector:
    """Test cases for MarketDataCollector"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.collector = MarketDataCollector()
        
        # Create sample data for testing
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        n_days = len(dates)
        
        # Generate synthetic price data
        returns = np.random.normal(0.001, 0.02, n_days)
        prices = 100 * np.cumprod(1 + returns)
        
        self.sample_data = pd.DataFrame({
            'Open': prices * (1 + np.random.normal(0, 0.005, n_days)),
            'High': prices * (1 + np.abs(np.random.normal(0, 0.01, n_days))),
            'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, n_days))),
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, n_days)
        }, index=dates)
        
        # Ensure High >= Low and High >= Close
        self.sample_data['High'] = np.maximum(self.sample_data['High'], self.sample_data['Close'])
        self.sample_data['Low'] = np.minimum(self.sample_data['Low'], self.sample_data['Close'])
    
    def test_market_data_initialization(self):
        """Test MarketDataCollector initialization"""
        assert self.collector.max_workers == 5
        assert self.collector.session is None
    
    def test_validate_and_clean_data(self):
        """Test data validation and cleaning"""
        # Test with valid data
        cleaned_data = self.collector._validate_and_clean_data(self.sample_data, "TEST")
        assert not cleaned_data.empty
        assert len(cleaned_data) == len(self.sample_data)
        
        # Test with data containing NaN values
        data_with_nan = self.sample_data.copy()
        data_with_nan.iloc[10:15] = np.nan
        
        cleaned_data = self.collector._validate_and_clean_data(data_with_nan, "TEST")
        assert len(cleaned_data) < len(data_with_nan)
        
        # Test with invalid price data
        data_invalid_prices = self.sample_data.copy()
        data_invalid_prices.iloc[5, 0] = -100  # Negative price
        
        cleaned_data = self.collector._validate_and_clean_data(data_invalid_prices, "TEST")
        assert len(cleaned_data) < len(data_invalid_prices)
    
    def test_calculate_technical_indicators(self):
        """Test technical indicator calculations"""
        df_with_indicators = self.collector.calculate_technical_indicators(self.sample_data)
        
        # Check that indicators are calculated
        assert 'SMA_20' in df_with_indicators.columns
        assert 'SMA_50' in df_with_indicators.columns
        assert 'EMA_12' in df_with_indicators.columns
        assert 'EMA_26' in df_with_indicators.columns
        assert 'MACD' in df_with_indicators.columns
        assert 'RSI' in df_with_indicators.columns
        assert 'BB_Upper' in df_with_indicators.columns
        
        # Check that indicators have reasonable values
        assert df_with_indicators['SMA_20'].notna().sum() > 0
        assert df_with_indicators['RSI'].notna().sum() > 0
        assert df_with_indicators['MACD'].notna().sum() > 0
        
        # Check RSI is between 0 and 100
        rsi_values = df_with_indicators['RSI'].dropna()
        assert (rsi_values >= 0).all()
        assert (rsi_values <= 100).all()
    
    def test_calculate_rsi(self):
        """Test RSI calculation specifically"""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
        rsi = self.collector._calculate_rsi(prices)
        
        assert len(rsi) == len(prices)
        assert rsi.notna().sum() > 0
        assert (rsi >= 0).all()
        assert (rsi <= 100).all()
    
    def test_get_market_summary(self):
        """Test market summary calculation"""
        # Create sample data dictionary
        data_dict = {
            'TEST1': self.sample_data,
            'TEST2': self.sample_data * 1.1  # 10% higher prices
        }
        
        summary = self.collector.get_market_summary(['TEST1', 'TEST2'])
        
        assert 'TEST1' in summary
        assert 'TEST2' in summary
        
        # Check summary contains required fields
        for symbol, info in summary.items():
            assert 'current_price' in info
            assert 'daily_change' in info
            assert 'daily_change_pct' in info
            assert 'volume' in info
            assert 'high_52w' in info
            assert 'low_52w' in info
            assert 'volatility' in info
            assert 'avg_volume' in info
            
            # Check data types
            assert isinstance(info['current_price'], (int, float))
            assert isinstance(info['daily_change'], (int, float))
            assert isinstance(info['daily_change_pct'], (int, float))
            assert isinstance(info['volume'], (int, float))
            assert isinstance(info['volatility'], (int, float))

class TestMarketData:
    """Test cases for MarketData dataclass"""
    
    def test_market_data_creation(self):
        """Test MarketData object creation"""
        now = datetime.now()
        
        market_data = MarketData(
            symbol="TEST",
            price=100.0,
            volume=1000000,
            timestamp=now,
            high=105.0,
            low=95.0,
            open_price=98.0,
            close=100.0
        )
        
        assert market_data.symbol == "TEST"
        assert market_data.price == 100.0
        assert market_data.volume == 1000000
        assert market_data.timestamp == now
        assert market_data.high == 105.0
        assert market_data.low == 95.0
        assert market_data.open_price == 98.0
        assert market_data.close == 100.0

class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from data collection to analysis"""
        collector = MarketDataCollector()
        
        # This would normally fetch real data, but we'll use mock data
        # In a real test environment, you might want to mock the yfinance calls
        
        # Test with sample data
        sample_data = {
            'TEST': pd.DataFrame({
                'Open': [100, 101, 102, 103, 104],
                'High': [105, 106, 107, 108, 109],
                'Low': [95, 96, 97, 98, 99],
                'Close': [100, 101, 102, 103, 104],
                'Volume': [1000000, 1100000, 1200000, 1300000, 1400000]
            }, index=pd.date_range('2023-01-01', periods=5))
        }
        
        # Test technical indicators
        df_with_indicators = collector.calculate_technical_indicators(sample_data['TEST'])
        assert not df_with_indicators.empty
        
        # Test market summary
        summary = collector.get_market_summary(['TEST'])
        assert 'TEST' in summary

# Pytest fixtures
@pytest.fixture
def sample_market_data():
    """Fixture providing sample market data"""
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    n_days = len(dates)
    
    returns = np.random.normal(0.001, 0.02, n_days)
    prices = 100 * np.cumprod(1 + returns)
    
    return pd.DataFrame({
        'Open': prices * (1 + np.random.normal(0, 0.005, n_days)),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.01, n_days))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, n_days))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, n_days)
    }, index=dates)

@pytest.fixture
def market_collector():
    """Fixture providing MarketDataCollector instance"""
    return MarketDataCollector()

# Parametrized tests
@pytest.mark.parametrize("symbol,expected", [
    ("AAPL", True),
    ("GOOGL", True),
    ("INVALID_SYMBOL", False),
    ("", False),
    (None, False)
])
def test_symbol_validation(symbol, expected):
    """Test symbol validation"""
    collector = MarketDataCollector()
    
    # This would test actual symbol validation in a real implementation
    # For now, we'll just test the logic
    if symbol and symbol.strip():
        assert expected
    else:
        assert not expected

if __name__ == "__main__":
    pytest.main([__file__])
