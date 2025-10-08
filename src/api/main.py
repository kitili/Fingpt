"""
FinGPT API
==========

REST API for FinGPT financial analysis services.
Demonstrates: API development, data serialization, error handling, async programming
"""

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.data.collectors.market_data import MarketDataCollector
from src.analysis.sentiment.financial_sentiment import FinancialSentimentAnalyzer
from src.models.optimization.portfolio_optimizer import PortfolioOptimizer
from src.analysis.trading.backtesting import Backtester, MovingAverageStrategy, RSIStrategy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FinGPT API",
    description="Financial analysis API demonstrating CS applications in finance",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class MarketDataRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of stock symbols")
    period: str = Field(default="1y", description="Time period for data")

class SentimentAnalysisRequest(BaseModel):
    text: str = Field(..., description="Text to analyze")
    
class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to analyze")

class PortfolioOptimizationRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of stock symbols")
    risk_free_rate: float = Field(default=0.02, description="Risk-free rate")
    method: str = Field(default="max_sharpe", description="Optimization method")

class BacktestRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol to backtest")
    strategy: str = Field(default="moving_average", description="Trading strategy")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    initial_cash: float = Field(default=100000, description="Initial cash")

class MarketDataResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    polarity: float
    confidence: float
    compound_score: float

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]
    summary: Dict[str, float]

class PortfolioResponse(BaseModel):
    method: str
    weights: Dict[str, float]
    expected_return: float
    volatility: float
    sharpe_ratio: float
    optimization_time: float

class BacktestResponse(BaseModel):
    strategy: str
    symbol: str
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    trades: List[Dict[str, Any]]

# Dependency injection
def get_market_collector():
    return MarketDataCollector()

def get_sentiment_analyzer():
    return FinancialSentimentAnalyzer()

def get_portfolio_optimizer():
    return PortfolioOptimizer()

def get_backtester():
    return Backtester()

# API Routes

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FinGPT API - CS Solutions in Finance",
        "version": "1.0.0",
        "endpoints": {
            "market_data": "/api/market-data",
            "sentiment": "/api/sentiment",
            "portfolio": "/api/portfolio",
            "backtest": "/api/backtest"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/market-data", response_model=MarketDataResponse)
async def get_market_data(
    request: MarketDataRequest,
    collector: MarketDataCollector = Depends(get_market_collector)
):
    """
    Get market data for specified symbols
    Demonstrates: API integration, data serialization, error handling
    """
    try:
        # Fetch market data
        data = collector.get_multiple_stocks(request.symbols, request.period)
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found for the specified symbols")
        
        # Calculate technical indicators for first symbol
        first_symbol = list(data.keys())[0]
        df_with_indicators = collector.calculate_technical_indicators(data[first_symbol])
        
        # Get market summary
        summary = collector.get_market_summary(request.symbols)
        
        # Prepare response data
        response_data = {
            "symbols": list(data.keys()),
            "summary": summary,
            "technical_indicators": {
                first_symbol: {
                    "sma_20": df_with_indicators['SMA_20'].iloc[-1] if 'SMA_20' in df_with_indicators.columns else None,
                    "sma_50": df_with_indicators['SMA_50'].iloc[-1] if 'SMA_50' in df_with_indicators.columns else None,
                    "rsi": df_with_indicators['RSI'].iloc[-1] if 'RSI' in df_with_indicators.columns else None,
                    "macd": df_with_indicators['MACD'].iloc[-1] if 'MACD' in df_with_indicators.columns else None
                }
            }
        }
        
        return MarketDataResponse(
            success=True,
            data=response_data,
            message=f"Successfully fetched data for {len(data)} symbols"
        )
        
    except Exception as e:
        logger.error(f"Error fetching market data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching market data: {str(e)}")

@app.post("/api/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    analyzer: FinancialSentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Analyze sentiment of financial text
    Demonstrates: NLP processing, sentiment analysis, text processing
    """
    try:
        result = analyzer.analyze_financial_sentiment(request.text)
        
        return SentimentResponse(
            text=result.text,
            sentiment=result.sentiment_label,
            polarity=result.polarity,
            confidence=result.confidence,
            compound_score=result.compound_score
        )
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@app.post("/api/sentiment/batch", response_model=BatchSentimentResponse)
async def analyze_batch_sentiment(
    request: BatchSentimentRequest,
    analyzer: FinancialSentimentAnalyzer = Depends(get_sentiment_analyzer)
):
    """
    Analyze sentiment for multiple texts
    Demonstrates: Batch processing, parallel analysis
    """
    try:
        results = analyzer.analyze_batch(request.texts)
        summary = analyzer.get_sentiment_summary(results)
        
        sentiment_responses = [
            SentimentResponse(
                text=result.text,
                sentiment=result.sentiment_label,
                polarity=result.polarity,
                confidence=result.confidence,
                compound_score=result.compound_score
            )
            for result in results
        ]
        
        return BatchSentimentResponse(
            results=sentiment_responses,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error analyzing batch sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing batch sentiment: {str(e)}")

@app.post("/api/portfolio/optimize", response_model=PortfolioResponse)
async def optimize_portfolio(
    request: PortfolioOptimizationRequest,
    collector: MarketDataCollector = Depends(get_market_collector),
    optimizer: PortfolioOptimizer = Depends(get_portfolio_optimizer)
):
    """
    Optimize portfolio using specified method
    Demonstrates: Portfolio optimization, mathematical programming
    """
    try:
        # Fetch market data
        data = collector.get_multiple_stocks(request.symbols, "1y")
        
        if not data:
            raise HTTPException(status_code=404, detail="No data found for the specified symbols")
        
        # Prepare data for optimization
        optimizer.risk_free_rate = request.risk_free_rate
        optimizer.prepare_data(data)
        
        # Run optimization based on method
        logger.info(f"Running optimization method: {request.method}")
        if request.method == "max_sharpe":
            result = optimizer.optimize_maximum_sharpe_ratio()
        elif request.method == "min_variance":
            result = optimizer.optimize_minimum_variance()
        elif request.method == "risk_parity":
            logger.info("Calling risk_parity_optimization method")
            result = optimizer.risk_parity_optimization()
        else:
            raise HTTPException(status_code=400, detail="Invalid optimization method")
        
        if not result:
            raise HTTPException(status_code=500, detail="Optimization failed")
        
        # Prepare weights dictionary
        weights_dict = {
            symbol: float(weight) 
            for symbol, weight in zip(result.weights.symbols, result.weights.weights)
        }
        
        return PortfolioResponse(
            method=result.optimization_method,
            weights=weights_dict,
            expected_return=float(result.weights.expected_return),
            volatility=float(result.weights.volatility),
            sharpe_ratio=float(result.weights.sharpe_ratio),
            optimization_time=float(result.optimization_time)
        )
        
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error optimizing portfolio: {str(e)}")

@app.post("/api/backtest", response_model=BacktestResponse)
async def run_backtest(
    request: BacktestRequest,
    collector: MarketDataCollector = Depends(get_market_collector),
    backtester: Backtester = Depends(get_backtester)
):
    """
    Run backtest for specified strategy and symbol
    Demonstrates: Strategy backtesting, performance analysis
    """
    try:
        # Fetch market data
        data = collector.get_stock_data(request.symbol, "1y")
        
        if data is None or data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {request.symbol}")
        
        # Filter data by date range
        start_date = pd.to_datetime(request.start_date)
        end_date = pd.to_datetime(request.end_date)
        # Convert index to datetime if needed and handle timezone
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)
        # Remove timezone info for comparison
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)
        data = data[(data.index >= start_date) & (data.index <= end_date)]
        
        if data.empty:
            raise HTTPException(status_code=400, detail="No data available for the specified date range")
        
        # Initialize strategy
        if request.strategy == "moving_average":
            strategy = MovingAverageStrategy()
        elif request.strategy == "rsi":
            strategy = RSIStrategy()
        else:
            raise HTTPException(status_code=400, detail="Invalid strategy")
        
        # Set initial cash
        backtester.initial_cash = request.initial_cash
        
        # Run backtest
        result = backtester.run_backtest(strategy, data, request.symbol)
        
        # Prepare trades data
        trades_data = [
            {
                "entry_date": trade.entry_date.isoformat(),
                "exit_date": trade.exit_date.isoformat(),
                "entry_price": float(trade.entry_price),
                "exit_price": float(trade.exit_price),
                "quantity": int(trade.quantity),
                "pnl": float(trade.pnl),
                "pnl_pct": float(trade.pnl_pct),
                "holding_period": int(trade.holding_period)
            }
            for trade in result.trades
        ]
        
        return BacktestResponse(
            strategy=request.strategy,
            symbol=request.symbol,
            total_return=float(result.total_return),
            annualized_return=float(result.annualized_return),
            volatility=float(result.volatility),
            sharpe_ratio=float(result.sharpe_ratio),
            max_drawdown=float(result.max_drawdown),
            win_rate=float(result.win_rate),
            total_trades=int(result.total_trades),
            trades=trades_data
        )
        
    except Exception as e:
        logger.error(f"Error running backtest: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error running backtest: {str(e)}")

@app.get("/api/strategies")
async def get_available_strategies():
    """Get list of available trading strategies"""
    return {
        "strategies": [
            {
                "name": "moving_average",
                "description": "Moving Average Crossover Strategy",
                "parameters": ["short_window", "long_window"]
            },
            {
                "name": "rsi",
                "description": "RSI-based Strategy",
                "parameters": ["rsi_period", "oversold", "overbought"]
            }
        ]
    }

@app.get("/api/optimization-methods")
async def get_optimization_methods():
    """Get list of available portfolio optimization methods"""
    return {
        "methods": [
            {
                "name": "max_sharpe",
                "description": "Maximum Sharpe Ratio Optimization"
            },
            {
                "name": "min_variance",
                "description": "Minimum Variance Optimization"
            },
            {
                "name": "risk_parity",
                "description": "Risk Parity Optimization"
            }
        ]
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": str(exc.detail) if hasattr(exc, 'detail') else str(exc)}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
