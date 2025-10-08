import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Input, Button, Select, Space, Typography, Spin, message, Table, Statistic } from 'antd';
import { LineChartOutlined, BarChartOutlined, TrendingUpOutlined } from '@ant-design/icons';
import Plot from 'react-plotly.js';

const { Title, Text } = Typography;
const { Option } = Select;

const TechnicalAnalysis = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [period, setPeriod] = useState('1y');
  const [loading, setLoading] = useState(false);
  const [marketData, setMarketData] = useState(null);
  const [indicators, setIndicators] = useState(null);

  const calculateRSI = (prices, period = 14) => {
    if (prices.length < period + 1) return [];
    
    const gains = [];
    const losses = [];
    
    for (let i = 1; i < prices.length; i++) {
      const change = prices[i] - prices[i - 1];
      gains.push(change > 0 ? change : 0);
      losses.push(change < 0 ? Math.abs(change) : 0);
    }
    
    const rsi = [];
    let avgGain = gains.slice(0, period).reduce((a, b) => a + b, 0) / period;
    let avgLoss = losses.slice(0, period).reduce((a, b) => a + b, 0) / period;
    
    for (let i = period; i < gains.length; i++) {
      avgGain = (avgGain * (period - 1) + gains[i]) / period;
      avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
      
      const rs = avgGain / avgLoss;
      const rsiValue = 100 - (100 / (1 + rs));
      rsi.push(rsiValue);
    }
    
    return rsi;
  };

  const calculateMACD = (prices, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
    if (prices.length < slowPeriod) return { macd: [], signal: [], histogram: [] };
    
    const emaFast = calculateEMA(prices, fastPeriod);
    const emaSlow = calculateEMA(prices, slowPeriod);
    
    const macd = emaFast.map((fast, i) => fast - emaSlow[i]);
    const signal = calculateEMA(macd, signalPeriod);
    const histogram = macd.map((macdVal, i) => macdVal - signal[i]);
    
    return { macd, signal, histogram };
  };

  const calculateEMA = (prices, period) => {
    const multiplier = 2 / (period + 1);
    const ema = [prices[0]];
    
    for (let i = 1; i < prices.length; i++) {
      ema.push((prices[i] * multiplier) + (ema[i - 1] * (1 - multiplier)));
    }
    
    return ema;
  };

  const calculateBollingerBands = (prices, period = 20, stdDev = 2) => {
    if (prices.length < period) return { upper: [], middle: [], lower: [] };
    
    const sma = [];
    const upper = [];
    const lower = [];
    
    for (let i = period - 1; i < prices.length; i++) {
      const slice = prices.slice(i - period + 1, i + 1);
      const mean = slice.reduce((a, b) => a + b, 0) / period;
      const variance = slice.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / period;
      const std = Math.sqrt(variance);
      
      sma.push(mean);
      upper.push(mean + (std * stdDev));
      lower.push(mean - (std * stdDev));
    }
    
    return { upper, middle: sma, lower };
  };

  const fetchTechnicalAnalysis = async () => {
    if (!symbol.trim()) {
      message.error('Please enter a symbol');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/market-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbols: [symbol], period })
      });

      const result = await response.json();
      
      if (result.success && result.data && result.data.data) {
        const data = result.data.data[symbol];
        if (data && data.historical_data) {
          const prices = data.historical_data.map(d => d.close);
          const dates = data.historical_data.map(d => d.date);
          
          // Calculate technical indicators
          const rsi = calculateRSI(prices);
          const macd = calculateMACD(prices);
          const bollinger = calculateBollingerBands(prices);
          
          setMarketData({
            prices,
            dates,
            historical: data.historical_data
          });
          
          setIndicators({
            rsi: rsi.slice(-100), // Last 100 values
            macd: {
              macd: macd.macd.slice(-100),
              signal: macd.signal.slice(-100),
              histogram: macd.histogram.slice(-100)
            },
            bollinger: {
              upper: bollinger.upper.slice(-100),
              middle: bollinger.middle.slice(-100),
              lower: bollinger.lower.slice(-100)
            }
          });
        } else {
          message.error('No historical data available');
        }
      } else {
        message.error('Failed to fetch market data');
      }
    } catch (error) {
      console.error('Error:', error);
      message.error('Error fetching technical analysis data');
    } finally {
      setLoading(false);
    }
  };

  const createPriceChart = () => {
    if (!marketData) return null;

    return {
      data: [{
        x: marketData.dates.slice(-100),
        y: marketData.prices.slice(-100),
        type: 'scatter',
        mode: 'lines',
        name: 'Price',
        line: { color: '#1890ff' }
      }],
      layout: {
        title: `${symbol} Price Chart`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price ($)' },
        height: 400
      }
    };
  };

  const createRSIChart = () => {
    if (!indicators || !marketData) return null;

    return {
      data: [{
        x: marketData.dates.slice(-100),
        y: indicators.rsi,
        type: 'scatter',
        mode: 'lines',
        name: 'RSI',
        line: { color: '#52c41a' }
      }, {
        x: marketData.dates.slice(-100),
        y: Array(indicators.rsi.length).fill(70),
        type: 'scatter',
        mode: 'lines',
        name: 'Overbought (70)',
        line: { color: 'red', dash: 'dash' }
      }, {
        x: marketData.dates.slice(-100),
        y: Array(indicators.rsi.length).fill(30),
        type: 'scatter',
        mode: 'lines',
        name: 'Oversold (30)',
        line: { color: 'green', dash: 'dash' }
      }],
      layout: {
        title: 'RSI (Relative Strength Index)',
        xaxis: { title: 'Date' },
        yaxis: { title: 'RSI', range: [0, 100] },
        height: 300
      }
    };
  };

  const createMACDChart = () => {
    if (!indicators || !marketData) return null;

    return {
      data: [{
        x: marketData.dates.slice(-100),
        y: indicators.macd.macd,
        type: 'scatter',
        mode: 'lines',
        name: 'MACD',
        line: { color: '#1890ff' }
      }, {
        x: marketData.dates.slice(-100),
        y: indicators.macd.signal,
        type: 'scatter',
        mode: 'lines',
        name: 'Signal',
        line: { color: '#ff4d4f' }
      }, {
        x: marketData.dates.slice(-100),
        y: indicators.macd.histogram,
        type: 'bar',
        name: 'Histogram',
        marker: { color: '#52c41a' }
      }],
      layout: {
        title: 'MACD (Moving Average Convergence Divergence)',
        xaxis: { title: 'Date' },
        yaxis: { title: 'MACD' },
        height: 300
      }
    };
  };

  const createBollingerBandsChart = () => {
    if (!indicators || !marketData) return null;

    return {
      data: [{
        x: marketData.dates.slice(-100),
        y: marketData.prices.slice(-100),
        type: 'scatter',
        mode: 'lines',
        name: 'Price',
        line: { color: '#1890ff' }
      }, {
        x: marketData.dates.slice(-100),
        y: indicators.bollinger.upper,
        type: 'scatter',
        mode: 'lines',
        name: 'Upper Band',
        line: { color: 'red', dash: 'dash' }
      }, {
        x: marketData.dates.slice(-100),
        y: indicators.bollinger.middle,
        type: 'scatter',
        mode: 'lines',
        name: 'Middle Band (SMA)',
        line: { color: 'orange' }
      }, {
        x: marketData.dates.slice(-100),
        y: indicators.bollinger.lower,
        type: 'scatter',
        mode: 'lines',
        name: 'Lower Band',
        line: { color: 'green', dash: 'dash' }
      }],
      layout: {
        title: 'Bollinger Bands',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price ($)' },
        height: 400
      }
    };
  };

  const getRSISignal = () => {
    if (!indicators || indicators.rsi.length === 0) return 'N/A';
    
    const currentRSI = indicators.rsi[indicators.rsi.length - 1];
    if (currentRSI > 70) return 'Overbought';
    if (currentRSI < 30) return 'Oversold';
    return 'Neutral';
  };

  const getMACDSignal = () => {
    if (!indicators || indicators.macd.macd.length < 2) return 'N/A';
    
    const macd = indicators.macd.macd;
    const signal = indicators.macd.signal;
    const currentMACD = macd[macd.length - 1];
    const currentSignal = signal[signal.length - 1];
    const prevMACD = macd[macd.length - 2];
    const prevSignal = signal[signal.length - 2];
    
    if (currentMACD > currentSignal && prevMACD <= prevSignal) return 'Bullish Crossover';
    if (currentMACD < currentSignal && prevMACD >= prevSignal) return 'Bearish Crossover';
    return 'No Signal';
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <TrendingUpOutlined /> Technical Analysis
      </Title>
      
      <Card style={{ marginBottom: '24px' }}>
        <Space size="large">
          <Input
            placeholder="Enter symbol (e.g., AAPL)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            style={{ width: 200 }}
          />
          <Select value={period} onChange={setPeriod} style={{ width: 120 }}>
            <Option value="1d">1 Day</Option>
            <Option value="5d">5 Days</Option>
            <Option value="1mo">1 Month</Option>
            <Option value="3mo">3 Months</Option>
            <Option value="6mo">6 Months</Option>
            <Option value="1y">1 Year</Option>
          </Select>
          <Button type="primary" onClick={fetchTechnicalAnalysis} loading={loading}>
            <BarChartOutlined /> Analyze
          </Button>
        </Space>
      </Card>

      {loading && (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>Analyzing technical indicators...</div>
        </div>
      )}

      {marketData && indicators && (
        <>
          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            <Col span={8}>
              <Card>
                <Statistic
                  title="RSI Signal"
                  value={getRSISignal()}
                  valueStyle={{ 
                    color: getRSISignal() === 'Overbought' ? '#ff4d4f' : 
                           getRSISignal() === 'Oversold' ? '#52c41a' : '#1890ff' 
                  }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="MACD Signal"
                  value={getMACDSignal()}
                  valueStyle={{ 
                    color: getMACDSignal().includes('Bullish') ? '#52c41a' : 
                           getMACDSignal().includes('Bearish') ? '#ff4d4f' : '#1890ff' 
                  }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="Current RSI"
                  value={indicators.rsi[indicators.rsi.length - 1]?.toFixed(2) || 'N/A'}
                  suffix=""
                />
              </Card>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col span={24}>
              <Card title="Price Chart" style={{ marginBottom: '16px' }}>
                <Plot {...createPriceChart()} />
              </Card>
            </Col>
          </Row>

          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Card title="RSI Indicator">
                <Plot {...createRSIChart()} />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="MACD Indicator">
                <Plot {...createMACDChart()} />
              </Card>
            </Col>
          </Row>

          <Row gutter={[16, 16]} style={{ marginTop: '16px' }}>
            <Col span={24}>
              <Card title="Bollinger Bands">
                <Plot {...createBollingerBandsChart()} />
              </Card>
            </Col>
          </Row>
        </>
      )}
    </div>
  );
};

export default TechnicalAnalysis;
