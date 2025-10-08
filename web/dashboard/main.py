"""
FinGPT Dashboard
===============

A Streamlit web application that demonstrates CS applications in finance.
This dashboard showcases various financial analysis tools and visualizations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
import yfinance as yf

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.data.collectors.market_data import MarketDataCollector
from src.analysis.sentiment.financial_sentiment import FinancialSentimentAnalyzer
from src.models.optimization.portfolio_optimizer import PortfolioOptimizer

# Page configuration
st.set_page_config(
    page_title="FinGPT for Everyone",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        color: #28a745;
    }
    .warning-metric {
        color: #ffc107;
    }
    .danger-metric {
        color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 FinGPT for Everyone</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">CS Solutions in Finance</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Market Overview", "Sentiment Analysis", "Portfolio Optimization", "Risk Analysis", "About"]
    )
    
    # Route to different pages
    if page == "Market Overview":
        market_overview_page()
    elif page == "Sentiment Analysis":
        sentiment_analysis_page()
    elif page == "Portfolio Optimization":
        portfolio_optimization_page()
    elif page == "Risk Analysis":
        risk_analysis_page()
    elif page == "About":
        about_page()

def market_overview_page():
    """Market Overview Dashboard"""
    st.markdown('<h2 class="section-header">📈 Market Overview</h2>', unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbols_input = st.text_input(
            "Enter stock symbols (comma-separated):",
            value="AAPL,GOOGL,MSFT,AMZN,TSLA",
            help="Enter stock symbols separated by commas"
        )
    
    with col2:
        period = st.selectbox(
            "Time Period:",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3
        )
    
    if st.button("Analyze Market", type="primary"):
        with st.spinner("Fetching market data..."):
            # Parse symbols
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            
            # Initialize collector
            collector = MarketDataCollector()
            
            # Fetch data
            data = collector.get_multiple_stocks(symbols, period)
            
            if data:
                st.success(f"Successfully fetched data for {len(data)} symbols")
                
                # Display market summary
                st.markdown('<h3 class="section-header">Market Summary</h3>', unsafe_allow_html=True)
                summary = collector.get_market_summary(symbols)
                
                # Create metrics
                cols = st.columns(len(summary))
                for i, (symbol, info) in enumerate(summary.items()):
                    with cols[i]:
                        change_color = "success-metric" if info['daily_change_pct'] >= 0 else "danger-metric"
                        st.metric(
                            label=symbol,
                            value=f"${info['current_price']:.2f}",
                            delta=f"{info['daily_change_pct']:+.2f}%"
                        )
                
                # Price charts
                st.markdown('<h3 class="section-header">Price Charts</h3>', unsafe_allow_html=True)
                
                # Create subplots
                fig = make_subplots(
                    rows=len(data), cols=1,
                    subplot_titles=list(data.keys()),
                    vertical_spacing=0.05
                )
                
                for i, (symbol, df) in enumerate(data.items()):
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df['Close'],
                            mode='lines',
                            name=symbol,
                            line=dict(color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)])
                        ),
                        row=i+1, col=1
                    )
                
                fig.update_layout(
                    height=200 * len(data),
                    showlegend=False,
                    title="Stock Price Trends"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                st.markdown('<h3 class="section-header">Technical Analysis</h3>', unsafe_allow_html=True)
                
                selected_symbol = st.selectbox("Select symbol for technical analysis:", list(data.keys()))
                
                if selected_symbol in data:
                    df_with_indicators = collector.calculate_technical_indicators(data[selected_symbol])
                    
                    # Create technical indicators chart
                    fig_tech = make_subplots(
                        rows=3, cols=1,
                        subplot_titles=["Price & Moving Averages", "RSI", "MACD"],
                        vertical_spacing=0.1
                    )
                    
                    # Price and moving averages
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['Close'], 
                                 name='Close', line=dict(color='blue')),
                        row=1, col=1
                    )
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['SMA_20'], 
                                 name='SMA 20', line=dict(color='orange')),
                        row=1, col=1
                    )
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['SMA_50'], 
                                 name='SMA 50', line=dict(color='red')),
                        row=1, col=1
                    )
                    
                    # RSI
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['RSI'], 
                                 name='RSI', line=dict(color='purple')),
                        row=2, col=1
                    )
                    fig_tech.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                    fig_tech.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
                    
                    # MACD
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['MACD'], 
                                 name='MACD', line=dict(color='blue')),
                        row=3, col=1
                    )
                    fig_tech.add_trace(
                        go.Scatter(x=df_with_indicators.index, y=df_with_indicators['MACD_Signal'], 
                                 name='Signal', line=dict(color='red')),
                        row=3, col=1
                    )
                    
                    fig_tech.update_layout(height=800, showlegend=True)
                    st.plotly_chart(fig_tech, use_container_width=True)
            else:
                st.error("Failed to fetch market data. Please check your symbols and try again.")

def sentiment_analysis_page():
    """Sentiment Analysis Dashboard"""
    st.markdown('<h2 class="section-header">😊 Sentiment Analysis</h2>', unsafe_allow_html=True)
    
    # Input section
    st.markdown("### Enter Financial Text for Analysis")
    
    text_input = st.text_area(
        "Enter financial news, tweets, or any financial text:",
        value="Apple's quarterly earnings exceeded expectations with strong iPhone sales, driving the stock price higher.",
        height=100
    )
    
    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Analyzing sentiment..."):
            # Initialize analyzer
            analyzer = FinancialSentimentAnalyzer()
            
            # Analyze sentiment
            result = analyzer.analyze_financial_sentiment(text_input)
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Sentiment",
                    result.sentiment_label.title(),
                    delta=f"{result.polarity:.3f}"
                )
            
            with col2:
                st.metric(
                    "Confidence",
                    f"{result.confidence:.1%}",
                    delta=f"{result.subjectivity:.3f}"
                )
            
            with col3:
                st.metric(
                    "Compound Score",
                    f"{result.compound_score:.3f}",
                    delta="VADER Analysis"
                )
            
            # Detailed analysis
            st.markdown("### Detailed Analysis")
            
            # Create gauge chart for polarity
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = result.polarity,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Sentiment Polarity"},
                delta = {'reference': 0},
                gauge = {
                    'axis': {'range': [-1, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-1, -0.1], 'color': "lightgray"},
                        {'range': [-0.1, 0.1], 'color': "yellow"},
                        {'range': [0.1, 1], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0
                    }
                }
            ))
            
            fig_gauge.update_layout(height=400)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
            # Batch analysis example
            st.markdown("### Batch Analysis Example")
            
            sample_texts = [
                "The market is showing strong bullish momentum",
                "Investors are concerned about the economic outlook",
                "Company earnings beat expectations significantly",
                "Stock prices remain volatile amid uncertainty"
            ]
            
            batch_results = analyzer.analyze_batch(sample_texts)
            summary = analyzer.get_sentiment_summary(batch_results)
            
            # Display batch results
            batch_df = pd.DataFrame([
                {
                    'Text': result.text,
                    'Sentiment': result.sentiment_label,
                    'Polarity': result.polarity,
                    'Confidence': result.confidence
                }
                for result in batch_results
            ])
            
            st.dataframe(batch_df, use_container_width=True)
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Polarity", f"{summary['avg_polarity']:.3f}")
            with col2:
                st.metric("Positive Ratio", f"{summary['positive_ratio']:.1%}")
            with col3:
                st.metric("Negative Ratio", f"{summary['negative_ratio']:.1%}")
            with col4:
                st.metric("Avg Confidence", f"{summary['avg_confidence']:.1%}")

def portfolio_optimization_page():
    """Portfolio Optimization Dashboard"""
    st.markdown('<h2 class="section-header">⚖️ Portfolio Optimization</h2>', unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbols_input = st.text_input(
            "Enter stock symbols for portfolio:",
            value="AAPL,GOOGL,MSFT,AMZN,TSLA",
            help="Enter stock symbols separated by commas"
        )
    
    with col2:
        risk_free_rate = st.number_input(
            "Risk-free Rate (%):",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.1
        ) / 100
    
    if st.button("Optimize Portfolio", type="primary"):
        with st.spinner("Optimizing portfolio..."):
            # Parse symbols
            symbols = [s.strip().upper() for s in symbols_input.split(",")]
            
            # Initialize collector and optimizer
            collector = MarketDataCollector()
            optimizer = PortfolioOptimizer(risk_free_rate=risk_free_rate)
            
            # Fetch data
            data = collector.get_multiple_stocks(symbols, "1y")
            
            if data:
                # Prepare data for optimization
                optimizer.prepare_data(data)
                
                # Run different optimization methods
                results = optimizer.compare_optimization_methods()
                
                # Display results
                st.markdown("### Optimization Results")
                
                for method_name, result in results.items():
                    if result:
                        with st.expander(f"{method_name.replace('_', ' ').title()}"):
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Expected Return", f"{result.weights.expected_return:.2%}")
                            with col2:
                                st.metric("Volatility", f"{result.weights.volatility:.2%}")
                            with col3:
                                st.metric("Sharpe Ratio", f"{result.weights.sharpe_ratio:.3f}")
                            with col4:
                                st.metric("Optimization Time", f"{result.optimization_time:.3f}s")
                            
                            # Portfolio weights
                            weights_df = pd.DataFrame({
                                'Symbol': result.weights.symbols,
                                'Weight': result.weights.weights,
                                'Weight %': result.weights.weights * 100
                            })
                            
                            st.dataframe(weights_df, use_container_width=True)
                            
                            # Weight visualization
                            fig_weights = px.pie(
                                weights_df, 
                                values='Weight', 
                                names='Symbol',
                                title=f"Portfolio Weights - {method_name.replace('_', ' ').title()}"
                            )
                            st.plotly_chart(fig_weights, use_container_width=True)
                
                # Efficient frontier
                st.markdown("### Efficient Frontier")
                
                frontier = optimizer.efficient_frontier(n_portfolios=50)
                
                fig_frontier = go.Figure()
                
                # Plot efficient frontier
                fig_frontier.add_trace(go.Scatter(
                    x=frontier['volatilities'],
                    y=frontier['returns'],
                    mode='markers',
                    name='Efficient Frontier',
                    marker=dict(color=frontier['sharpe_ratios'], 
                              colorscale='Viridis',
                              showscale=True,
                              colorbar=dict(title="Sharpe Ratio"))
                ))
                
                # Highlight optimal portfolios
                for method_name, result in results.items():
                    if result:
                        fig_frontier.add_trace(go.Scatter(
                            x=[result.weights.volatility],
                            y=[result.weights.expected_return],
                            mode='markers',
                            name=method_name.replace('_', ' ').title(),
                            marker=dict(size=15, symbol='star')
                        ))
                
                fig_frontier.update_layout(
                    title="Efficient Frontier",
                    xaxis_title="Volatility",
                    yaxis_title="Expected Return",
                    height=600
                )
                
                st.plotly_chart(fig_frontier, use_container_width=True)
                
                # Monte Carlo analysis
                st.markdown("### Monte Carlo Analysis")
                
                mc_results = optimizer.monte_carlo_optimization(n_simulations=5000)
                
                fig_mc = go.Figure()
                
                fig_mc.add_trace(go.Scatter(
                    x=mc_results['volatilities'],
                    y=mc_results['returns'],
                    mode='markers',
                    name='Random Portfolios',
                    marker=dict(
                        color=mc_results['sharpe_ratios'],
                        colorscale='Viridis',
                        size=5,
                        opacity=0.6
                    )
                ))
                
                # Add efficient frontier
                fig_mc.add_trace(go.Scatter(
                    x=frontier['volatilities'],
                    y=frontier['returns'],
                    mode='lines',
                    name='Efficient Frontier',
                    line=dict(color='red', width=3)
                ))
                
                fig_mc.update_layout(
                    title="Monte Carlo Portfolio Simulation",
                    xaxis_title="Volatility",
                    yaxis_title="Expected Return",
                    height=600
                )
                
                st.plotly_chart(fig_mc, use_container_width=True)
                
                # Monte Carlo statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Best Sharpe Ratio", f"{mc_results['sharpe_ratios'].max():.3f}")
                with col2:
                    st.metric("Average Sharpe Ratio", f"{mc_results['sharpe_ratios'].mean():.3f}")
                with col3:
                    st.metric("Worst Sharpe Ratio", f"{mc_results['sharpe_ratios'].min():.3f}")
            else:
                st.error("Failed to fetch market data. Please check your symbols and try again.")

def risk_analysis_page():
    """Risk Analysis Dashboard"""
    st.markdown('<h2 class="section-header">⚠️ Risk Analysis</h2>', unsafe_allow_html=True)
    
    st.info("Risk analysis features will be implemented in future versions. This will include VaR calculations, stress testing, and scenario analysis.")
    
    # Placeholder content
    st.markdown("### Coming Soon: Advanced Risk Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Value at Risk (VaR)**
        - Historical VaR
        - Parametric VaR
        - Monte Carlo VaR
        
        **Conditional Value at Risk (CVaR)**
        - Expected shortfall
        - Tail risk analysis
        """)
    
    with col2:
        st.markdown("""
        **Stress Testing**
        - Historical scenarios
        - Hypothetical scenarios
        - Sensitivity analysis
        
        **Risk Attribution**
        - Factor analysis
        - Sector exposure
        - Geographic exposure
        """)

def about_page():
    """About Page"""
    st.markdown('<h2 class="section-header">About FinGPT for Everyone</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎯 Mission
    
    FinGPT for Everyone demonstrates how computer science expertise can be applied to solve real-world financial problems. This project showcases various CS concepts including:
    
    ### 🔧 Computer Science Concepts Applied
    
    - **Data Structures & Algorithms**: Efficient data processing, sorting, searching
    - **Machine Learning**: Predictive modeling, classification, regression
    - **Optimization**: Linear programming, convex optimization, Monte Carlo methods
    - **Natural Language Processing**: Sentiment analysis, text processing
    - **Web Development**: REST APIs, real-time dashboards, data visualization
    - **Database Systems**: Data storage, query optimization
    - **Software Engineering**: Modular design, testing, error handling
    
    ### 📊 Financial Applications
    
    - **Market Data Analysis**: Real-time data collection and processing
    - **Sentiment Analysis**: News and social media sentiment analysis
    - **Portfolio Optimization**: Modern portfolio theory implementation
    - **Risk Assessment**: Statistical risk modeling
    - **Technical Analysis**: Technical indicators and charting
    - **Performance Analytics**: Portfolio performance metrics
    
    ### 🚀 Technology Stack
    
    - **Python**: Core programming language
    - **Pandas/NumPy**: Data manipulation and analysis
    - **Scikit-learn**: Machine learning algorithms
    - **Streamlit**: Web application framework
    - **Plotly**: Interactive visualizations
    - **yfinance**: Financial data API
    - **CVXPY**: Convex optimization
    
    ### 🎓 Educational Value
    
    This project serves as a comprehensive example of how computer science skills can be applied in the financial sector, making it valuable for:
    
    - CS students learning practical applications
    - Finance professionals exploring technology solutions
    - Anyone interested in the intersection of technology and finance
    
    ### 🤝 Contributing
    
    This is an open-source educational project. Contributions, suggestions, and improvements are welcome!
    """)
    
    st.markdown("---")
    st.markdown("**Built with ❤️ using Computer Science principles**")

if __name__ == "__main__":
    main()
