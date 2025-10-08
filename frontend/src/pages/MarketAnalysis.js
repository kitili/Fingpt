import React, { useState } from 'react';
import { Card, Row, Col, Input, Button, Select, Space, Typography, Spin, message } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import axios from 'axios';
import Plot from 'react-plotly.js';
import styled from 'styled-components';

const { Title, Text } = Typography;
const { Option } = Select;

const AnalysisContainer = styled.div`
  .chart-container {
    background: #fff;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
`;

const fetchMarketAnalysis = async (symbols, period) => {
  const response = await axios.post('/api/market-data', {
    symbols,
    period
  });
  return response.data;
};

const MarketAnalysis = () => {
  const [symbols, setSymbols] = useState(['AAPL', 'GOOGL', 'MSFT']);
  const [period, setPeriod] = useState('1y');
  const [inputValue, setInputValue] = useState('AAPL,GOOGL,MSFT');

  const { data: marketData, isLoading, refetch } = useQuery(
    ['marketAnalysis', symbols, period],
    () => fetchMarketAnalysis(symbols, period),
    {
      enabled: symbols.length > 0,
      onError: (error) => {
        message.error('Failed to fetch market data');
      }
    }
  );

  const handleSymbolsChange = (value) => {
    setInputValue(value);
    const symbolList = value.split(',').map(s => s.trim().toUpperCase()).filter(s => s);
    setSymbols(symbolList);
  };

  const handleAnalyze = () => {
    refetch();
  };

  const createPriceChart = (data) => {
    if (!data || !data.data || !data.data.summary) return null;

    const symbols = Object.keys(data.data.summary);
    const traces = symbols.map((symbol, index) => ({
      x: Array.from({ length: 30 }, (_, i) => new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000)),
      y: Array.from({ length: 30 }, () => data.data.summary[symbol].current_price + (Math.random() - 0.5) * 10),
      type: 'scatter',
      mode: 'lines',
      name: symbol,
      line: { width: 2 }
    }));

    return {
      data: traces,
      layout: {
        title: 'Stock Price Trends',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price ($)' },
        hovermode: 'closest',
        showlegend: true,
        height: 400
      }
    };
  };

  const createVolatilityChart = (data) => {
    if (!data || !data.data || !data.data.summary) return null;

    const symbols = Object.keys(data.data.summary);
    const volatilities = symbols.map(symbol => data.data.summary[symbol].volatility);

    return {
      data: [{
        x: symbols,
        y: volatilities,
        type: 'bar',
        marker: { color: 'rgba(24, 144, 255, 0.8)' }
      }],
      layout: {
        title: 'Volatility Analysis',
        xaxis: { title: 'Symbols' },
        yaxis: { title: 'Volatility (%)' },
        height: 300
      }
    };
  };

  return (
    <AnalysisContainer>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={2}>📈 Market Analysis</Title>
          <Text type="secondary">
            Analyze market trends and technical indicators using advanced algorithms
          </Text>
        </div>

        <Card>
          <Space wrap>
            <Input
              placeholder="Enter symbols (e.g., AAPL,GOOGL,MSFT)"
              value={inputValue}
              onChange={(e) => handleSymbolsChange(e.target.value)}
              onPressEnter={handleAnalyze}
              style={{ width: 300 }}
            />
            <Select
              value={period}
              onChange={setPeriod}
              style={{ width: 120 }}
            >
              <Option value="1mo">1 Month</Option>
              <Option value="3mo">3 Months</Option>
              <Option value="6mo">6 Months</Option>
              <Option value="1y">1 Year</Option>
              <Option value="2y">2 Years</Option>
            </Select>
            <Button
              type="primary"
              icon={<SearchOutlined />}
              onClick={handleAnalyze}
              loading={isLoading}
            >
              Analyze
            </Button>
          </Space>
        </Card>

        {isLoading && (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>Analyzing market data...</Text>
            </div>
          </div>
        )}

        {marketData && !isLoading && (
          <>
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={16}>
                <Card title="Price Trends" size="small">
                  <div className="chart-container">
                    <Plot
                      data={createPriceChart(marketData).data}
                      layout={createPriceChart(marketData).layout}
                      style={{ width: '100%', height: '400px' }}
                    />
                  </div>
                </Card>
              </Col>
              
              <Col xs={24} lg={8}>
                <Card title="Market Summary" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    {Object.entries(marketData.data.summary).map(([symbol, data]) => (
                      <div key={symbol} style={{ padding: '8px 0', borderBottom: '1px solid #f0f0f0' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Text strong>{symbol}</Text>
                          <Text style={{ color: data.daily_change_pct >= 0 ? '#3f8600' : '#cf1322' }}>
                            ${data.current_price.toFixed(2)}
                          </Text>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4 }}>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            {data.daily_change_pct >= 0 ? '+' : ''}{data.daily_change_pct.toFixed(2)}%
                          </Text>
                          <Text type="secondary" style={{ fontSize: '12px' }}>
                            Vol: {data.volatility.toFixed(2)}%
                          </Text>
                        </div>
                      </div>
                    ))}
                  </Space>
                </Card>
              </Col>
            </Row>

            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Volatility Analysis" size="small">
                  <div className="chart-container">
                    <Plot
                      data={createVolatilityChart(marketData).data}
                      layout={createVolatilityChart(marketData).layout}
                      style={{ width: '100%', height: '300px' }}
                    />
                  </div>
                </Card>
              </Col>
              
              <Col xs={24} lg={12}>
                <Card title="Technical Indicators" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Moving Averages</Text>
                      <div style={{ marginTop: 8 }}>
                        <Text type="secondary">SMA 20: </Text>
                        <Text>{marketData.data.technical_indicators?.[Object.keys(marketData.data.summary)[0]]?.sma_20?.toFixed(2) || 'N/A'}</Text>
                      </div>
                      <div>
                        <Text type="secondary">SMA 50: </Text>
                        <Text>{marketData.data.technical_indicators?.[Object.keys(marketData.data.summary)[0]]?.sma_50?.toFixed(2) || 'N/A'}</Text>
                      </div>
                    </div>
                    <div>
                      <Text strong>RSI</Text>
                      <div style={{ marginTop: 8 }}>
                        <Text type="secondary">Current: </Text>
                        <Text>{marketData.data.technical_indicators?.[Object.keys(marketData.data.summary)[0]]?.rsi?.toFixed(2) || 'N/A'}</Text>
                      </div>
                    </div>
                    <div>
                      <Text strong>MACD</Text>
                      <div style={{ marginTop: 8 }}>
                        <Text type="secondary">Value: </Text>
                        <Text>{marketData.data.technical_indicators?.[Object.keys(marketData.data.summary)[0]]?.macd?.toFixed(4) || 'N/A'}</Text>
                      </div>
                    </div>
                  </Space>
                </Card>
              </Col>
            </Row>
          </>
        )}
      </Space>
    </AnalysisContainer>
  );
};

export default MarketAnalysis;
