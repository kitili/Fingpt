"""
Market Data Collector
====================

This module demonstrates how CS concepts like API integration, data structures,
and error handling can be applied to collect financial market data efficiently.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Data class representing market data - demonstrates OOP principles"""
    symbol: str
    price: float
    volume: int
    timestamp: datetime
    high: float
    low: float
    open_price: float
    close: float

class MarketDataCollector:
    """
    Market Data Collector using CS principles:
    - Object-oriented design
    - Error handling and resilience
    - Concurrent data collection
    - Data validation and type safety
    """
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.session = None
        
    async def __aenter__(self):
        """Async context manager for resource management"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch stock data using yfinance
        Demonstrates: Error handling, data validation, API integration
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for symbol: {symbol}")
                return None
                
            # Data validation and cleaning
            data = self._validate_and_clean_data(data, symbol)
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def _validate_and_clean_data(self, data: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """
        Data validation and cleaning
        Demonstrates: Data quality assurance, preprocessing
        """
        # Remove any rows with NaN values
        data = data.dropna()
        
        # Ensure we have required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            logger.error(f"Missing columns for {symbol}: {missing_columns}")
            return pd.DataFrame()
        
        # Validate price data (no negative prices)
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if (data[col] <= 0).any():
                logger.warning(f"Invalid price data in {col} for {symbol}")
                data = data[data[col] > 0]
        
        # Validate volume data
        if (data['Volume'] < 0).any():
            logger.warning(f"Invalid volume data for {symbol}")
            data = data[data['Volume'] >= 0]
        
        return data
    
    def get_multiple_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks concurrently
        Demonstrates: Concurrent programming, thread pools, resource management
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(self.get_stock_data, symbol, period): symbol 
                for symbol in symbols
            }
            
            # Collect results as they complete
            for future in future_to_symbol:
                symbol = future_to_symbol[future]
                try:
                    data = future.result(timeout=30)  # 30 second timeout
                    if data is not None:
                        results[symbol] = data
                    else:
                        logger.warning(f"Failed to fetch data for {symbol}")
                except Exception as e:
                    logger.error(f"Exception for {symbol}: {str(e)}")
        
        return results
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators
        Demonstrates: Mathematical algorithms, data transformation
        """
        df = data.copy()
        
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # RSI (Relative Strength Index)
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """
        Calculate RSI using efficient pandas operations
        Demonstrates: Algorithm implementation, vectorized operations
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_market_summary(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Get market summary for multiple symbols
        Demonstrates: Data aggregation, statistical analysis
        """
        data_dict = self.get_multiple_stocks(symbols)
        summary = {}
        
        for symbol, data in data_dict.items():
            if data.empty:
                continue
                
            latest = data.iloc[-1]
            summary[symbol] = {
                'current_price': latest['Close'],
                'daily_change': latest['Close'] - data.iloc[-2]['Close'] if len(data) > 1 else 0,
                'daily_change_pct': ((latest['Close'] - data.iloc[-2]['Close']) / data.iloc[-2]['Close'] * 100) if len(data) > 1 else 0,
                'volume': latest['Volume'],
                'high_52w': data['High'].max(),
                'low_52w': data['Low'].min(),
                'volatility': data['Close'].pct_change().std() * np.sqrt(252),  # Annualized volatility
                'avg_volume': data['Volume'].mean()
            }
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    # Demonstrate the collector
    collector = MarketDataCollector()
    
    # Get data for popular tech stocks
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    print("Fetching market data...")
    data = collector.get_multiple_stocks(symbols)
    
    print(f"Successfully fetched data for {len(data)} symbols")
    
    # Calculate technical indicators for first symbol
    if data:
        first_symbol = list(data.keys())[0]
        df_with_indicators = collector.calculate_technical_indicators(data[first_symbol])
        print(f"\nTechnical indicators calculated for {first_symbol}")
        print(df_with_indicators[['Close', 'SMA_20', 'RSI', 'MACD']].tail())
    
    # Get market summary
    summary = collector.get_market_summary(symbols)
    print(f"\nMarket Summary:")
    for symbol, info in summary.items():
        print(f"{symbol}: ${info['current_price']:.2f} ({info['daily_change_pct']:+.2f}%)")
