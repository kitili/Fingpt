"""
Trading Strategy Backtesting Framework
=====================================

This module demonstrates how CS concepts like algorithms, data structures,
and statistical analysis can be applied to backtest trading strategies.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Callable, Any
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class Trade:
    """Data class representing a single trade"""
    entry_date: datetime
    exit_date: datetime
    symbol: str
    side: str  # 'long' or 'short'
    entry_price: float
    exit_price: float
    quantity: int
    pnl: float
    pnl_pct: float
    holding_period: int

@dataclass
class BacktestResult:
    """Data class for backtest results"""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    avg_trade_return: float
    trades: List[Trade]

class TradingStrategy:
    """
    Base class for trading strategies
    Demonstrates: Object-oriented design, strategy pattern, inheritance
    """
    
    def __init__(self, name: str):
        self.name = name
        self.positions = {}  # Current positions
        self.trades = []     # Completed trades
        self.cash = 100000   # Starting cash
        self.initial_cash = 100000
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals
        To be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement generate_signals")
    
    def should_buy(self, data: pd.DataFrame, index: int) -> bool:
        """Check if we should buy at given index"""
        return False
    
    def should_sell(self, data: pd.DataFrame, index: int, position: Dict) -> bool:
        """Check if we should sell at given index"""
        return False
    
    def calculate_position_size(self, price: float, signal_strength: float = 1.0) -> int:
        """Calculate position size based on available cash and signal strength"""
        # Simple position sizing: use 10% of available cash
        max_position_value = self.cash * 0.1 * signal_strength
        return int(max_position_value / price)

class MovingAverageStrategy(TradingStrategy):
    """
    Simple Moving Average Crossover Strategy
    Demonstrates: Technical analysis, signal generation, algorithmic trading
    """
    
    def __init__(self, short_window: int = 20, long_window: int = 50):
        super().__init__("Moving Average Crossover")
        self.short_window = short_window
        self.long_window = long_window
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on moving average crossover"""
        df = data.copy()
        
        # Calculate moving averages
        df['SMA_short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        df['Signal'] = 0
        df['Signal'][self.short_window:] = np.where(
            df['SMA_short'][self.short_window:] > df['SMA_long'][self.short_window:], 1, 0
        )
        
        # Generate position changes
        df['Position'] = df['Signal'].diff()
        
        return df
    
    def should_buy(self, data: pd.DataFrame, index: int) -> bool:
        """Buy when short MA crosses above long MA"""
        if index < self.long_window:
            return False
        
        current_signal = data['Signal'].iloc[index]
        previous_signal = data['Signal'].iloc[index - 1]
        
        return current_signal == 1 and previous_signal == 0
    
    def should_sell(self, data: pd.DataFrame, index: int, position: Dict) -> bool:
        """Sell when short MA crosses below long MA"""
        if index < self.long_window:
            return False
        
        current_signal = data['Signal'].iloc[index]
        previous_signal = data['Signal'].iloc[index - 1]
        
        return current_signal == 0 and previous_signal == 1

class RSIStrategy(TradingStrategy):
    """
    RSI-based Trading Strategy
    Demonstrates: Technical indicators, overbought/oversold conditions
    """
    
    def __init__(self, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
        super().__init__("RSI Strategy")
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate RSI-based signals"""
        df = data.copy()
        df['RSI'] = self.calculate_rsi(df['Close'])
        
        # Generate signals
        df['Signal'] = 0
        df['Signal'] = np.where(df['RSI'] < self.oversold, 1,  # Buy when oversold
                       np.where(df['RSI'] > self.overbought, -1, 0))  # Sell when overbought
        
        df['Position'] = df['Signal'].diff()
        
        return df
    
    def should_buy(self, data: pd.DataFrame, index: int) -> bool:
        """Buy when RSI crosses above oversold level"""
        if index < self.rsi_period:
            return False
        
        current_rsi = data['RSI'].iloc[index]
        previous_rsi = data['RSI'].iloc[index - 1]
        
        return current_rsi > self.oversold and previous_rsi <= self.oversold
    
    def should_sell(self, data: pd.DataFrame, index: int, position: Dict) -> bool:
        """Sell when RSI crosses below overbought level"""
        if index < self.rsi_period:
            return False
        
        current_rsi = data['RSI'].iloc[index]
        previous_rsi = data['RSI'].iloc[index - 1]
        
        return current_rsi < self.overbought and previous_rsi >= self.overbought

class Backtester:
    """
    Backtesting Engine
    Demonstrates: Event-driven programming, portfolio management, performance analysis
    """
    
    def __init__(self, initial_cash: float = 100000, commission: float = 0.001):
        self.initial_cash = initial_cash
        self.commission = commission
        self.reset()
    
    def reset(self):
        """Reset backtester state"""
        self.cash = self.initial_cash
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        self.dates = []
    
    def run_backtest(self, strategy: TradingStrategy, data: pd.DataFrame, 
                    symbol: str = "STOCK") -> BacktestResult:
        """
        Run backtest for a given strategy and data
        Demonstrates: Event simulation, portfolio tracking, performance calculation
        """
        self.reset()
        
        # Generate signals
        data_with_signals = strategy.generate_signals(data)
        
        # Simulate trading
        for i in range(len(data_with_signals)):
            current_date = data_with_signals.index[i]
            current_price = data_with_signals['Close'].iloc[i]
            
            # Check for buy signals
            if strategy.should_buy(data_with_signals, i):
                self._execute_buy(symbol, current_price, current_date, data_with_signals, i)
            
            # Check for sell signals
            if symbol in self.positions:
                if strategy.should_sell(data_with_signals, i, self.positions[symbol]):
                    self._execute_sell(symbol, current_price, current_date)
            
            # Update equity curve
            self._update_equity_curve(symbol, current_price, current_date)
        
        # Close any remaining positions
        if symbol in self.positions:
            final_price = data_with_signals['Close'].iloc[-1]
            final_date = data_with_signals.index[-1]
            self._execute_sell(symbol, final_price, final_date)
        
        # Calculate performance metrics
        return self._calculate_performance()
    
    def _execute_buy(self, symbol: str, price: float, date: datetime, 
                    data: pd.DataFrame, index: int):
        """Execute buy order"""
        if symbol in self.positions:
            return  # Already have position
        
        # Calculate position size
        signal_strength = abs(data['Signal'].iloc[index]) if 'Signal' in data.columns else 1.0
        quantity = self._calculate_position_size(price, signal_strength)
        
        if quantity > 0:
            cost = quantity * price * (1 + self.commission)
            
            if cost <= self.cash:
                self.positions[symbol] = {
                    'quantity': quantity,
                    'entry_price': price,
                    'entry_date': date,
                    'entry_cost': cost
                }
                self.cash -= cost
                
                logger.info(f"BUY: {quantity} shares of {symbol} at ${price:.2f} on {date.date()}")
    
    def _execute_sell(self, symbol: str, price: float, date: datetime):
        """Execute sell order"""
        if symbol not in self.positions:
            return
        
        position = self.positions[symbol]
        quantity = position['quantity']
        proceeds = quantity * price * (1 - self.commission)
        
        # Calculate P&L
        pnl = proceeds - position['entry_cost']
        pnl_pct = (price - position['entry_price']) / position['entry_price']
        holding_period = (date - position['entry_date']).days
        
        # Record trade
        trade = Trade(
            entry_date=position['entry_date'],
            exit_date=date,
            symbol=symbol,
            side='long',
            entry_price=position['entry_price'],
            exit_price=price,
            quantity=quantity,
            pnl=pnl,
            pnl_pct=pnl_pct,
            holding_period=holding_period
        )
        
        self.trades.append(trade)
        self.cash += proceeds
        
        logger.info(f"SELL: {quantity} shares of {symbol} at ${price:.2f} on {date.date()}, P&L: ${pnl:.2f} ({pnl_pct:.2%})")
        
        # Remove position
        del self.positions[symbol]
    
    def _calculate_position_size(self, price: float, signal_strength: float = 1.0) -> int:
        """Calculate position size based on available cash"""
        max_position_value = self.cash * 0.1 * signal_strength  # Use 10% of cash
        return int(max_position_value / price)
    
    def _update_equity_curve(self, symbol: str, price: float, date: datetime):
        """Update equity curve"""
        total_value = self.cash
        
        if symbol in self.positions:
            position_value = self.positions[symbol]['quantity'] * price
            total_value += position_value
        
        self.equity_curve.append(total_value)
        self.dates.append(date)
    
    def _calculate_performance(self) -> BacktestResult:
        """Calculate performance metrics"""
        if not self.equity_curve:
            return BacktestResult(0, 0, 0, 0, 0, 0, 0, 0, 0, [])
        
        # Convert to numpy arrays for easier calculation
        equity = np.array(self.equity_curve)
        dates = np.array(self.dates)
        
        # Calculate returns
        returns = np.diff(equity) / equity[:-1]
        
        # Total return
        total_return = (equity[-1] - equity[0]) / equity[0]
        
        # Annualized return
        days = (dates[-1] - dates[0]).days
        annualized_return = (1 + total_return) ** (365 / days) - 1
        
        # Volatility (annualized)
        volatility = np.std(returns) * np.sqrt(252)
        
        # Sharpe ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Maximum drawdown
        peak = np.maximum.accumulate(equity)
        drawdown = (equity - peak) / peak
        max_drawdown = np.min(drawdown)
        
        # Trade statistics
        if self.trades:
            winning_trades = [t for t in self.trades if t.pnl > 0]
            losing_trades = [t for t in self.trades if t.pnl < 0]
            
            win_rate = len(winning_trades) / len(self.trades)
            
            total_wins = sum(t.pnl for t in winning_trades)
            total_losses = abs(sum(t.pnl for t in losing_trades))
            profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            avg_trade_return = np.mean([t.pnl_pct for t in self.trades])
        else:
            win_rate = 0
            profit_factor = 0
            avg_trade_return = 0
        
        return BacktestResult(
            total_return=total_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(self.trades),
            avg_trade_return=avg_trade_return,
            trades=self.trades
        )
    
    def plot_results(self, result: BacktestResult, data: pd.DataFrame, 
                    symbol: str = "STOCK") -> go.Figure:
        """
        Plot backtest results
        Demonstrates: Data visualization, performance analysis
        """
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=[
                f"{symbol} Price and Signals",
                "Equity Curve",
                "Drawdown"
            ],
            vertical_spacing=0.1,
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # Price chart with signals
        fig.add_trace(
            go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Add buy/sell signals
        if 'Signal' in data.columns:
            buy_signals = data[data['Signal'] == 1]
            sell_signals = data[data['Signal'] == -1]
            
            if not buy_signals.empty:
                fig.add_trace(
                    go.Scatter(x=buy_signals.index, y=buy_signals['Close'],
                              mode='markers', name='Buy Signal', marker=dict(color='green', size=8)),
                    row=1, col=1
                )
            
            if not sell_signals.empty:
                fig.add_trace(
                    go.Scatter(x=sell_signals.index, y=sell_signals['Close'],
                              mode='markers', name='Sell Signal', marker=dict(color='red', size=8)),
                    row=1, col=1
                )
        
        # Equity curve
        if self.equity_curve:
            fig.add_trace(
                go.Scatter(x=self.dates, y=self.equity_curve, name='Equity', line=dict(color='green')),
                row=2, col=1
            )
        
        # Drawdown
        if self.equity_curve:
            peak = np.maximum.accumulate(self.equity_curve)
            drawdown = (np.array(self.equity_curve) - peak) / peak * 100
            
            fig.add_trace(
                go.Scatter(x=self.dates, y=drawdown, name='Drawdown %', 
                          fill='tonexty', line=dict(color='red')),
                row=3, col=1
            )
        
        fig.update_layout(
            title=f"Backtest Results - {symbol}",
            height=800,
            showlegend=True
        )
        
        return fig

# Example usage and testing
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    n_days = len(dates)
    
    # Generate synthetic price data with trend and volatility
    returns = np.random.normal(0.0005, 0.02, n_days)  # Daily returns
    prices = 100 * np.cumprod(1 + returns)  # Starting price of $100
    
    data = pd.DataFrame({
        'Close': prices,
        'Open': prices * (1 + np.random.normal(0, 0.005, n_days)),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.01, n_days))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, n_days))),
        'Volume': np.random.randint(1000000, 5000000, n_days)
    }, index=dates)
    
    # Ensure High >= Low and High >= Close
    data['High'] = np.maximum(data['High'], data['Close'])
    data['Low'] = np.minimum(data['Low'], data['Close'])
    
    print("Backtesting Demo")
    print("=" * 50)
    
    # Test Moving Average Strategy
    print("\n1. Moving Average Crossover Strategy:")
    ma_strategy = MovingAverageStrategy(short_window=20, long_window=50)
    backtester = Backtester()
    
    ma_result = backtester.run_backtest(ma_strategy, data, "TEST")
    
    print(f"Total Return: {ma_result.total_return:.2%}")
    print(f"Annualized Return: {ma_result.annualized_return:.2%}")
    print(f"Volatility: {ma_result.volatility:.2%}")
    print(f"Sharpe Ratio: {ma_result.sharpe_ratio:.3f}")
    print(f"Max Drawdown: {ma_result.max_drawdown:.2%}")
    print(f"Win Rate: {ma_result.win_rate:.2%}")
    print(f"Total Trades: {ma_result.total_trades}")
    
    # Test RSI Strategy
    print("\n2. RSI Strategy:")
    rsi_strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)
    backtester.reset()
    
    rsi_result = backtester.run_backtest(rsi_strategy, data, "TEST")
    
    print(f"Total Return: {rsi_result.total_return:.2%}")
    print(f"Annualized Return: {rsi_result.annualized_return:.2%}")
    print(f"Volatility: {rsi_result.volatility:.2%}")
    print(f"Sharpe Ratio: {rsi_result.sharpe_ratio:.3f}")
    print(f"Max Drawdown: {rsi_result.max_drawdown:.2%}")
    print(f"Win Rate: {rsi_result.win_rate:.2%}")
    print(f"Total Trades: {rsi_result.total_trades}")
    
    # Compare strategies
    print("\n3. Strategy Comparison:")
    strategies = {
        'Moving Average': ma_result,
        'RSI': rsi_result
    }
    
    comparison_df = pd.DataFrame({
        name: {
            'Total Return': f"{result.total_return:.2%}",
            'Sharpe Ratio': f"{result.sharpe_ratio:.3f}",
            'Max Drawdown': f"{result.max_drawdown:.2%}",
            'Win Rate': f"{result.win_rate:.2%}",
            'Total Trades': result.total_trades
        }
        for name, result in strategies.items()
    })
    
    print(comparison_df)
