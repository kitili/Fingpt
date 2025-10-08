"""
Portfolio Optimization
=====================

This module demonstrates how CS concepts like optimization algorithms,
linear algebra, and statistical analysis can be applied to portfolio management.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Union
import cvxpy as cp
from scipy.optimize import minimize
from scipy import stats
import logging
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class PortfolioWeights:
    """Data class for portfolio weights"""
    symbols: List[str]
    weights: np.ndarray
    expected_return: float
    volatility: float
    sharpe_ratio: float

@dataclass
class OptimizationResult:
    """Data class for optimization results"""
    weights: PortfolioWeights
    optimization_method: str
    constraints_satisfied: bool
    optimization_time: float

class PortfolioOptimizer:
    """
    Portfolio Optimizer using various CS techniques:
    - Linear programming and convex optimization
    - Statistical analysis and risk modeling
    - Algorithm design and optimization
    - Matrix operations and linear algebra
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate
        self.returns_data = None
        self.covariance_matrix = None
        self.expected_returns = None
        
    def prepare_data(self, price_data: Dict[str, pd.DataFrame]) -> None:
        """
        Prepare data for optimization
        Demonstrates: Data preprocessing, statistical calculations
        """
        # Calculate returns for each asset
        returns_dict = {}
        for symbol, data in price_data.items():
            if 'Close' in data.columns:
                returns = data['Close'].pct_change().dropna()
                returns_dict[symbol] = returns
        
        # Align all returns to same time period
        returns_df = pd.DataFrame(returns_dict)
        returns_df = returns_df.dropna()
        
        self.returns_data = returns_df
        self.expected_returns = returns_df.mean() * 252  # Annualized
        self.covariance_matrix = returns_df.cov() * 252  # Annualized
        
        logger.info(f"Prepared data for {len(returns_df.columns)} assets over {len(returns_df)} periods")
    
    def calculate_portfolio_metrics(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate portfolio metrics
        Demonstrates: Mathematical operations, statistical calculations
        """
        # Expected return
        portfolio_return = np.dot(weights, self.expected_returns)
        
        # Portfolio variance
        portfolio_variance = np.dot(weights.T, np.dot(self.covariance_matrix, weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        
        # Sharpe ratio
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def optimize_maximum_sharpe_ratio(self) -> OptimizationResult:
        """
        Optimize for maximum Sharpe ratio using convex optimization
        Demonstrates: Convex optimization, CVXPY, mathematical programming
        """
        import time
        start_time = time.time()
        
        n_assets = len(self.expected_returns)
        
        # Variables
        weights = cp.Variable(n_assets)
        
        # Expected return and risk
        portfolio_return = self.expected_returns.values @ weights
        portfolio_risk = cp.quad_form(weights, self.covariance_matrix.values)
        
        # Objective: maximize Sharpe ratio (minimize negative Sharpe)
        objective = cp.Maximize((portfolio_return - self.risk_free_rate) / cp.sqrt(portfolio_risk))
        
        # Constraints
        constraints = [
            cp.sum(weights) == 1,  # Weights sum to 1
            weights >= 0,  # No short selling
            weights <= 1   # No single asset > 100%
        ]
        
        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        optimization_time = time.time() - start_time
        
        if problem.status == "optimal":
            optimal_weights = weights.value
            expected_return, volatility, sharpe_ratio = self.calculate_portfolio_metrics(optimal_weights)
            
            return OptimizationResult(
                weights=PortfolioWeights(
                    symbols=list(self.expected_returns.index),
                    weights=optimal_weights,
                    expected_return=expected_return,
                    volatility=volatility,
                    sharpe_ratio=sharpe_ratio
                ),
                optimization_method="Maximum Sharpe Ratio",
                constraints_satisfied=True,
                optimization_time=optimization_time
            )
        else:
            logger.error(f"Optimization failed: {problem.status}")
            return None
    
    def optimize_minimum_variance(self) -> OptimizationResult:
        """
        Optimize for minimum variance portfolio
        Demonstrates: Quadratic programming, risk minimization
        """
        import time
        start_time = time.time()
        
        n_assets = len(self.expected_returns)
        
        # Variables
        weights = cp.Variable(n_assets)
        
        # Objective: minimize portfolio variance
        portfolio_risk = cp.quad_form(weights, self.covariance_matrix.values)
        objective = cp.Minimize(portfolio_risk)
        
        # Constraints
        constraints = [
            cp.sum(weights) == 1,  # Weights sum to 1
            weights >= 0,  # No short selling
            weights <= 1   # No single asset > 100%
        ]
        
        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        optimization_time = time.time() - start_time
        
        if problem.status == "optimal":
            optimal_weights = weights.value
            expected_return, volatility, sharpe_ratio = self.calculate_portfolio_metrics(optimal_weights)
            
            return OptimizationResult(
                weights=PortfolioWeights(
                    symbols=list(self.expected_returns.index),
                    weights=optimal_weights,
                    expected_return=expected_return,
                    volatility=volatility,
                    sharpe_ratio=sharpe_ratio
                ),
                optimization_method="Minimum Variance",
                constraints_satisfied=True,
                optimization_time=optimization_time
            )
        else:
            logger.error(f"Optimization failed: {problem.status}")
            return None
    
    def optimize_target_return(self, target_return: float) -> OptimizationResult:
        """
        Optimize for target return with minimum variance
        Demonstrates: Constrained optimization, target-based investing
        """
        import time
        start_time = time.time()
        
        n_assets = len(self.expected_returns)
        
        # Variables
        weights = cp.Variable(n_assets)
        
        # Objective: minimize portfolio variance
        portfolio_risk = cp.quad_form(weights, self.covariance_matrix.values)
        objective = cp.Minimize(portfolio_risk)
        
        # Constraints
        constraints = [
            cp.sum(weights) == 1,  # Weights sum to 1
            weights >= 0,  # No short selling
            weights <= 1,  # No single asset > 100%
            self.expected_returns.values @ weights >= target_return  # Target return
        ]
        
        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        optimization_time = time.time() - start_time
        
        if problem.status == "optimal":
            optimal_weights = weights.value
            expected_return, volatility, sharpe_ratio = self.calculate_portfolio_metrics(optimal_weights)
            
            return OptimizationResult(
                weights=PortfolioWeights(
                    symbols=list(self.expected_returns.index),
                    weights=optimal_weights,
                    expected_return=expected_return,
                    volatility=volatility,
                    sharpe_ratio=sharpe_ratio
                ),
                optimization_method=f"Target Return ({target_return:.2%})",
                constraints_satisfied=True,
                optimization_time=optimization_time
            )
        else:
            logger.error(f"Optimization failed: {problem.status}")
            return None
    
    def monte_carlo_optimization(self, n_simulations: int = 10000) -> Dict[str, np.ndarray]:
        """
        Monte Carlo portfolio optimization
        Demonstrates: Monte Carlo methods, random sampling, statistical analysis
        """
        n_assets = len(self.expected_returns)
        results = {
            'returns': np.zeros(n_simulations),
            'volatilities': np.zeros(n_simulations),
            'sharpe_ratios': np.zeros(n_simulations),
            'weights': np.zeros((n_simulations, n_assets))
        }
        
        for i in range(n_simulations):
            # Generate random weights
            random_weights = np.random.random(n_assets)
            random_weights = random_weights / np.sum(random_weights)  # Normalize
            
            # Calculate metrics
            expected_return, volatility, sharpe_ratio = self.calculate_portfolio_metrics(random_weights)
            
            results['returns'][i] = expected_return
            results['volatilities'][i] = volatility
            results['sharpe_ratios'][i] = sharpe_ratio
            results['weights'][i] = random_weights
        
        return results
    
    def efficient_frontier(self, n_portfolios: int = 100) -> Dict[str, np.ndarray]:
        """
        Generate efficient frontier
        Demonstrates: Mathematical optimization, frontier analysis
        """
        min_ret = self.expected_returns.min()
        max_ret = self.expected_returns.max()
        target_returns = np.linspace(min_ret, max_ret, n_portfolios)
        
        efficient_portfolios = {
            'returns': np.zeros(n_portfolios),
            'volatilities': np.zeros(n_portfolios),
            'sharpe_ratios': np.zeros(n_portfolios),
            'weights': np.zeros((n_portfolios, len(self.expected_returns)))
        }
        
        for i, target_ret in enumerate(target_returns):
            result = self.optimize_target_return(target_ret)
            if result and result.constraints_satisfied:
                efficient_portfolios['returns'][i] = result.weights.expected_return
                efficient_portfolios['volatilities'][i] = result.weights.volatility
                efficient_portfolios['sharpe_ratios'][i] = result.weights.sharpe_ratio
                efficient_portfolios['weights'][i] = result.weights.weights
        
        return efficient_portfolios
    
    def risk_parity_optimization(self) -> OptimizationResult:
        """
        Risk parity optimization
        Demonstrates: Alternative optimization approach, risk budgeting
        """
        import time
        start_time = time.time()
        
        n_assets = len(self.expected_returns)
        
        # Variables
        weights = cp.Variable(n_assets)
        
        # Risk contributions
        risk_contributions = cp.multiply(weights, (self.covariance_matrix.values @ weights))
        
        # Objective: minimize sum of squared deviations from equal risk contributions
        target_risk_contrib = cp.sum(risk_contributions) / n_assets
        objective = cp.Minimize(cp.sum_squares(risk_contributions - target_risk_contrib))
        
        # Constraints
        constraints = [
            cp.sum(weights) == 1,  # Weights sum to 1
            weights >= 0,  # No short selling
            weights <= 1   # No single asset > 100%
        ]
        
        # Solve
        problem = cp.Problem(objective, constraints)
        problem.solve()
        
        optimization_time = time.time() - start_time
        
        if problem.status == "optimal":
            optimal_weights = weights.value
            expected_return, volatility, sharpe_ratio = self.calculate_portfolio_metrics(optimal_weights)
            
            return OptimizationResult(
                weights=PortfolioWeights(
                    symbols=list(self.expected_returns.index),
                    weights=optimal_weights,
                    expected_return=expected_return,
                    volatility=volatility,
                    sharpe_ratio=sharpe_ratio
                ),
                optimization_method="Risk Parity",
                constraints_satisfied=True,
                optimization_time=optimization_time
            )
        else:
            logger.error(f"Risk parity optimization failed: {problem.status}")
            return None
    
    def compare_optimization_methods(self) -> Dict[str, OptimizationResult]:
        """
        Compare different optimization methods
        Demonstrates: Method comparison, performance analysis
        """
        methods = {}
        
        # Maximum Sharpe Ratio
        try:
            methods['max_sharpe'] = self.optimize_maximum_sharpe_ratio()
        except Exception as e:
            logger.error(f"Max Sharpe optimization failed: {str(e)}")
        
        # Minimum Variance
        try:
            methods['min_variance'] = self.optimize_minimum_variance()
        except Exception as e:
            logger.error(f"Min variance optimization failed: {str(e)}")
        
        # Risk Parity
        try:
            methods['risk_parity'] = self.risk_parity_optimization()
        except Exception as e:
            logger.error(f"Risk parity optimization failed: {str(e)}")
        
        return methods
    
    def calculate_portfolio_metrics_detailed(self, weights: np.ndarray) -> Dict[str, float]:
        """
        Calculate detailed portfolio metrics
        Demonstrates: Risk analysis, performance metrics
        """
        portfolio_return, portfolio_volatility, sharpe_ratio = self.calculate_portfolio_metrics(weights)
        
        # Additional metrics
        returns = self.returns_data @ weights
        portfolio_skewness = stats.skew(returns)
        portfolio_kurtosis = stats.kurtosis(returns)
        
        # Value at Risk (VaR) - 5% VaR
        var_95 = np.percentile(returns, 5)
        
        # Conditional Value at Risk (CVaR)
        cvar_95 = returns[returns <= var_95].mean()
        
        # Maximum Drawdown
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return {
            'expected_return': portfolio_return,
            'volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'skewness': portfolio_skewness,
            'kurtosis': portfolio_kurtosis,
            'var_95': var_95,
            'cvar_95': cvar_95,
            'max_drawdown': max_drawdown
        }

# Example usage and testing
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    n_assets = 5
    n_periods = 252
    
    # Generate synthetic returns data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    returns_data = pd.DataFrame(
        np.random.normal(0.001, 0.02, (n_periods, n_assets)),
        columns=symbols
    )
    
    # Create price data (for compatibility with prepare_data)
    price_data = {}
    for symbol in symbols:
        prices = (1 + returns_data[symbol]).cumprod() * 100
        price_data[symbol] = pd.DataFrame({'Close': prices})
    
    # Initialize optimizer
    optimizer = PortfolioOptimizer(risk_free_rate=0.02)
    optimizer.prepare_data(price_data)
    
    print("Portfolio Optimization Demo")
    print("=" * 50)
    
    # Compare optimization methods
    results = optimizer.compare_optimization_methods()
    
    for method_name, result in results.items():
        if result:
            print(f"\n{method_name.upper()}:")
            print(f"Expected Return: {result.weights.expected_return:.4f}")
            print(f"Volatility: {result.weights.volatility:.4f}")
            print(f"Sharpe Ratio: {result.weights.sharpe_ratio:.4f}")
            print(f"Optimization Time: {result.optimization_time:.4f}s")
            print("Weights:")
            for symbol, weight in zip(result.weights.symbols, result.weights.weights):
                print(f"  {symbol}: {weight:.4f}")
    
    # Monte Carlo analysis
    print(f"\n{'='*50}")
    print("MONTE CARLO ANALYSIS")
    print("="*50)
    
    mc_results = optimizer.monte_carlo_optimization(n_simulations=1000)
    print(f"Best Sharpe Ratio: {mc_results['sharpe_ratios'].max():.4f}")
    print(f"Average Sharpe Ratio: {mc_results['sharpe_ratios'].mean():.4f}")
    print(f"Worst Sharpe Ratio: {mc_results['sharpe_ratios'].min():.4f}")
    
    # Efficient frontier
    print(f"\n{'='*50}")
    print("EFFICIENT FRONTIER")
    print("="*50)
    
    frontier = optimizer.efficient_frontier(n_portfolios=20)
    print(f"Frontier portfolios generated: {len(frontier['returns'])}")
    print(f"Return range: {frontier['returns'].min():.4f} to {frontier['returns'].max():.4f}")
    print(f"Volatility range: {frontier['volatilities'].min():.4f} to {frontier['volatilities'].max():.4f}")
