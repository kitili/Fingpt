import React, { useState } from 'react';
import { Card, Row, Col, Input, Button, Select, Space, Typography, Spin, message, Table, Progress, Statistic } from 'antd';
import { WarningOutlined, SafetyOutlined, BarChartOutlined } from '@ant-design/icons';
import Plot from 'react-plotly.js';

const { Title, Text } = Typography;
const { Option } = Select;

const RiskAnalysis = () => {
  const [symbols, setSymbols] = useState(['AAPL', 'GOOGL', 'MSFT']);
  const [period, setPeriod] = useState('1y');
  const [loading, setLoading] = useState(false);
  const [riskMetrics, setRiskMetrics] = useState(null);
  const [correlationMatrix, setCorrelationMatrix] = useState(null);

  const calculateVaR = (returns, confidence = 0.05) => {
    if (returns.length === 0) return 0;
    const sortedReturns = [...returns].sort((a, b) => a - b);
    const index = Math.floor(confidence * sortedReturns.length);
    return Math.abs(sortedReturns[index] || 0);
  };

  const calculateCVaR = (returns, confidence = 0.05) => {
    if (returns.length === 0) return 0;
    const sortedReturns = [...returns].sort((a, b) => a - b);
    const varIndex = Math.floor(confidence * sortedReturns.length);
    const tailReturns = sortedReturns.slice(0, varIndex);
    return Math.abs(tailReturns.reduce((a, b) => a + b, 0) / tailReturns.length || 0);
  };

  const calculateMaxDrawdown = (prices) => {
    if (prices.length === 0) return 0;
    let maxPrice = prices[0];
    let maxDrawdown = 0;
    
    for (let i = 1; i < prices.length; i++) {
      if (prices[i] > maxPrice) {
        maxPrice = prices[i];
      }
      const drawdown = (maxPrice - prices[i]) / maxPrice;
      if (drawdown > maxDrawdown) {
        maxDrawdown = drawdown;
      }
    }
    
    return maxDrawdown;
  };

  const calculateSharpeRatio = (returns, riskFreeRate = 0.02) => {
    if (returns.length === 0) return 0;
    const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
    const volatility = Math.sqrt(returns.reduce((a, b) => a + Math.pow(b - avgReturn, 2), 0) / returns.length);
    return volatility === 0 ? 0 : (avgReturn - riskFreeRate / 252) / volatility;
  };

  const calculateCorrelationMatrix = (priceData) => {
    const symbols = Object.keys(priceData);
    const matrix = [];
    
    for (let i = 0; i < symbols.length; i++) {
      const row = [];
      for (let j = 0; j < symbols.length; j++) {
        if (i === j) {
          row.push(1);
        } else {
          const corr = calculateCorrelation(priceData[symbols[i]], priceData[symbols[j]]);
          row.push(corr);
        }
      }
      matrix.push(row);
    }
    
    return { matrix, symbols };
  };

  const calculateCorrelation = (prices1, prices2) => {
    if (prices1.length !== prices2.length || prices1.length === 0) return 0;
    
    const returns1 = prices1.slice(1).map((price, i) => (price - prices1[i]) / prices1[i]);
    const returns2 = prices2.slice(1).map((price, i) => (price - prices2[i]) / prices2[i]);
    
    const mean1 = returns1.reduce((a, b) => a + b, 0) / returns1.length;
    const mean2 = returns2.reduce((a, b) => a + b, 0) / returns2.length;
    
    let numerator = 0;
    let sumSq1 = 0;
    let sumSq2 = 0;
    
    for (let i = 0; i < returns1.length; i++) {
      const diff1 = returns1[i] - mean1;
      const diff2 = returns2[i] - mean2;
      numerator += diff1 * diff2;
      sumSq1 += diff1 * diff1;
      sumSq2 += diff2 * diff2;
    }
    
    const denominator = Math.sqrt(sumSq1 * sumSq2);
    return denominator === 0 ? 0 : numerator / denominator;
  };

  const fetchRiskAnalysis = async () => {
    if (symbols.length === 0) {
      message.error('Please enter at least one symbol');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/market-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbols, period })
      });

      const result = await response.json();
      
      if (result.success && result.data && result.data.data) {
        const data = result.data.data;
        const priceData = {};
        const riskMetricsData = {};
        
        // Process data for each symbol
        Object.keys(data).forEach(symbol => {
          const symbolData = data[symbol];
          if (symbolData && symbolData.historical_data) {
            const prices = symbolData.historical_data.map(d => d.close);
            const returns = prices.slice(1).map((price, i) => (price - prices[i]) / prices[i]);
            
            priceData[symbol] = prices;
            
            riskMetricsData[symbol] = {
              var95: calculateVaR(returns, 0.05),
              var99: calculateVaR(returns, 0.01),
              cvar95: calculateCVaR(returns, 0.05),
              cvar99: calculateCVaR(returns, 0.01),
              maxDrawdown: calculateMaxDrawdown(prices),
              sharpeRatio: calculateSharpeRatio(returns),
              volatility: Math.sqrt(returns.reduce((a, b) => a + Math.pow(b - returns.reduce((x, y) => x + y, 0) / returns.length, 2), 0) / returns.length) * Math.sqrt(252),
              avgReturn: returns.reduce((a, b) => a + b, 0) / returns.length * 252
            };
          }
        });
        
        setRiskMetrics(riskMetricsData);
        
        // Calculate correlation matrix
        if (Object.keys(priceData).length > 1) {
          const correlation = calculateCorrelationMatrix(priceData);
          setCorrelationMatrix(correlation);
        }
        
      } else {
        message.error('Failed to fetch market data');
      }
    } catch (error) {
      console.error('Error:', error);
      message.error('Error fetching risk analysis data');
    } finally {
      setLoading(false);
    }
  };

  const createCorrelationHeatmap = () => {
    if (!correlationMatrix) return null;

    return {
      data: [{
        z: correlationMatrix.matrix,
        x: correlationMatrix.symbols,
        y: correlationMatrix.symbols,
        type: 'heatmap',
        colorscale: 'RdBu',
        zmin: -1,
        zmax: 1,
        text: correlationMatrix.matrix.map(row => 
          row.map(val => val.toFixed(3))
        ),
        texttemplate: '%{text}',
        textfont: { size: 12 }
      }],
      layout: {
        title: 'Asset Correlation Matrix',
        xaxis: { title: 'Assets' },
        yaxis: { title: 'Assets' },
        height: 400
      }
    };
  };

  const getRiskLevel = (value, type) => {
    if (type === 'volatility') {
      if (value < 0.15) return { level: 'Low', color: '#52c41a' };
      if (value < 0.25) return { level: 'Medium', color: '#faad14' };
      return { level: 'High', color: '#ff4d4f' };
    }
    if (type === 'maxDrawdown') {
      if (value < 0.1) return { level: 'Low', color: '#52c41a' };
      if (value < 0.2) return { level: 'Medium', color: '#faad14' };
      return { level: 'High', color: '#ff4d4f' };
    }
    if (type === 'sharpeRatio') {
      if (value > 1) return { level: 'Excellent', color: '#52c41a' };
      if (value > 0.5) return { level: 'Good', color: '#1890ff' };
      if (value > 0) return { level: 'Fair', color: '#faad14' };
      return { level: 'Poor', color: '#ff4d4f' };
    }
    return { level: 'N/A', color: '#d9d9d9' };
  };

  const riskTableColumns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: 'Volatility',
      dataIndex: 'volatility',
      key: 'volatility',
      render: (value) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: 'VaR (95%)',
      dataIndex: 'var95',
      key: 'var95',
      render: (value) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: 'VaR (99%)',
      dataIndex: 'var99',
      key: 'var99',
      render: (value) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: 'Max Drawdown',
      dataIndex: 'maxDrawdown',
      key: 'maxDrawdown',
      render: (value) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: 'Sharpe Ratio',
      dataIndex: 'sharpeRatio',
      key: 'sharpeRatio',
      render: (value) => value.toFixed(3),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <WarningOutlined /> Risk Analysis
      </Title>
      
      <Card style={{ marginBottom: '24px' }}>
        <Space size="large" wrap>
          <Input
            placeholder="Enter symbols (e.g., AAPL,GOOGL,MSFT)"
            value={symbols.join(',')}
            onChange={(e) => setSymbols(e.target.value.split(',').map(s => s.trim().toUpperCase()).filter(s => s))}
            style={{ width: 300 }}
          />
          <Select value={period} onChange={setPeriod} style={{ width: 120 }}>
            <Option value="1mo">1 Month</Option>
            <Option value="3mo">3 Months</Option>
            <Option value="6mo">6 Months</Option>
            <Option value="1y">1 Year</Option>
          </Select>
          <Button type="primary" onClick={fetchRiskAnalysis} loading={loading}>
            <BarChartOutlined /> Analyze Risk
          </Button>
        </Space>
      </Card>

      {loading && (
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <Spin size="large" />
          <div style={{ marginTop: '16px' }}>Analyzing risk metrics...</div>
        </div>
      )}

      {riskMetrics && (
        <>
          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            {Object.entries(riskMetrics).map(([symbol, metrics]) => (
              <Col span={6} key={symbol}>
                <Card>
                  <Statistic
                    title={`${symbol} Risk Level`}
                    value={getRiskLevel(metrics.volatility, 'volatility').level}
                    valueStyle={{ 
                      color: getRiskLevel(metrics.volatility, 'volatility').color 
                    }}
                    prefix={<SafetyOutlined />}
                  />
                  <div style={{ marginTop: '8px' }}>
                    <Text type="secondary">Volatility: {(metrics.volatility * 100).toFixed(2)}%</Text>
                  </div>
                </Card>
              </Col>
            ))}
          </Row>

          <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
            <Col span={24}>
              <Card title="Risk Metrics Table">
                <Table
                  columns={riskTableColumns}
                  dataSource={Object.entries(riskMetrics).map(([symbol, metrics]) => ({
                    key: symbol,
                    symbol,
                    ...metrics
                  }))}
                  pagination={false}
                />
              </Card>
            </Col>
          </Row>

          {correlationMatrix && (
            <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
              <Col span={24}>
                <Card title="Asset Correlation Analysis">
                  <Plot {...createCorrelationHeatmap()} />
                </Card>
              </Col>
            </Row>
          )}

          <Row gutter={[16, 16]}>
            {Object.entries(riskMetrics).map(([symbol, metrics]) => (
              <Col span={8} key={symbol}>
                <Card title={`${symbol} Risk Breakdown`}>
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Volatility Risk:</Text>
                      <Progress 
                        percent={Math.min(metrics.volatility * 100, 100)} 
                        status={getRiskLevel(metrics.volatility, 'volatility').level === 'High' ? 'exception' : 'normal'}
                      />
                    </div>
                    <div>
                      <Text strong>Drawdown Risk:</Text>
                      <Progress 
                        percent={Math.min(metrics.maxDrawdown * 100, 100)} 
                        status={getRiskLevel(metrics.maxDrawdown, 'maxDrawdown').level === 'High' ? 'exception' : 'normal'}
                      />
                    </div>
                    <div>
                      <Text strong>Risk-Adjusted Return (Sharpe):</Text>
                      <Progress 
                        percent={Math.min(Math.max(metrics.sharpeRatio * 50 + 50, 0), 100)} 
                        status={getRiskLevel(metrics.sharpeRatio, 'sharpeRatio').level === 'Poor' ? 'exception' : 'normal'}
                      />
                    </div>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </>
      )}
    </div>
  );
};

export default RiskAnalysis;
