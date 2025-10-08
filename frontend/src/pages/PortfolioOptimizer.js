import React, { useState } from 'react';
import { Card, Row, Col, Input, Button, Select, Space, Typography, Spin, message, Table, Progress } from 'antd';
import { PieChartOutlined, LineChartOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import axios from 'axios';
import Plot from 'react-plotly.js';
import styled from 'styled-components';

const { Title, Text } = Typography;
const { Option } = Select;

const OptimizerContainer = styled.div`
  .optimization-card {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
`;

const fetchPortfolioOptimization = async (symbols, method, riskFreeRate) => {
  const response = await axios.post('/api/portfolio/optimize', {
    symbols,
    method,
    risk_free_rate: riskFreeRate
  });
  return response.data;
};

const PortfolioOptimizer = () => {
  const [symbols, setSymbols] = useState(['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']);
  const [method, setMethod] = useState('max_sharpe');
  const [riskFreeRate, setRiskFreeRate] = useState(0.02);
  const [inputValue, setInputValue] = useState('AAPL,GOOGL,MSFT,AMZN,TSLA');

  const { data: optimizationData, isLoading, refetch } = useQuery(
    ['portfolioOptimization', symbols, method, riskFreeRate],
    () => fetchPortfolioOptimization(symbols, method, riskFreeRate),
    {
      enabled: symbols.length > 0,
      onError: (error) => {
        message.error('Failed to optimize portfolio');
      }
    }
  );

  const handleSymbolsChange = (value) => {
    setInputValue(value);
    const symbolList = value.split(',').map(s => s.trim().toUpperCase()).filter(s => s);
    setSymbols(symbolList);
  };

  const handleOptimize = () => {
    refetch();
  };

  const createPieChart = (weights) => {
    if (!weights) return null;

    const data = Object.entries(weights).map(([symbol, weight]) => ({
      labels: symbol,
      values: weight * 100,
      type: 'pie'
    }));

    return {
      data: [{
        labels: Object.keys(weights),
        values: Object.values(weights).map(w => w * 100),
        type: 'pie',
        textinfo: 'label+percent',
        textposition: 'outside'
      }],
      layout: {
        title: 'Portfolio Allocation',
        height: 400,
        showlegend: true
      }
    };
  };

  const columns = [
    {
      title: 'Symbol',
      dataIndex: 'symbol',
      key: 'symbol',
    },
    {
      title: 'Weight',
      dataIndex: 'weight',
      key: 'weight',
      render: (weight) => `${(weight * 100).toFixed(2)}%`,
    },
    {
      title: 'Allocation',
      dataIndex: 'weight',
      key: 'allocation',
      render: (weight) => (
        <Progress 
          percent={weight * 100} 
          size="small" 
          strokeColor="#1890ff"
        />
      ),
    },
  ];

  const dataSource = optimizationData ? 
    Object.entries(optimizationData.weights).map(([symbol, weight], index) => ({
      key: index,
      symbol,
      weight
    })) : [];

  return (
    <OptimizerContainer>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={2}>⚖️ Portfolio Optimizer</Title>
          <Text type="secondary">
            Optimize your portfolio using advanced mathematical algorithms
          </Text>
        </div>

        <Card>
          <Space wrap>
            <Input
              placeholder="Enter symbols (e.g., AAPL,GOOGL,MSFT)"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onPressEnter={handleOptimize}
              style={{ width: 300 }}
            />
            <Select
              value={method}
              onChange={setMethod}
              style={{ width: 200 }}
            >
              <Option value="max_sharpe">Max Sharpe Ratio</Option>
              <Option value="min_variance">Min Variance</Option>
              <Option value="risk_parity">Risk Parity</Option>
            </Select>
            <Input
              placeholder="Risk-free Rate"
              value={riskFreeRate}
              onChange={(e) => setRiskFreeRate(parseFloat(e.target.value) || 0.02)}
              style={{ width: 150 }}
              suffix="%"
            />
            <Button
              type="primary"
              icon={<PieChartOutlined />}
              onClick={handleOptimize}
              loading={isLoading}
            >
              Optimize
            </Button>
          </Space>
        </Card>

        {isLoading && (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>Optimizing portfolio...</Text>
            </div>
          </div>
        )}

        {optimizationData && !isLoading && (
          <>
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Portfolio Allocation" size="small" className="optimization-card">
                  <div style={{ height: '400px' }}>
                    <Plot
                      data={createPieChart(optimizationData.weights).data}
                      layout={createPieChart(optimizationData.weights).layout}
                      style={{ width: '100%', height: '100%' }}
                    />
                  </div>
                </Card>
              </Col>
              
              <Col xs={24} lg={12}>
                <Card title="Optimization Results" size="small" className="optimization-card">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Method: </Text>
                      <Text>{optimizationData.method}</Text>
                    </div>
                    <div>
                      <Text strong>Expected Return: </Text>
                      <Text style={{ color: '#3f8600' }}>
                        {(optimizationData.expected_return * 100).toFixed(2)}%
                      </Text>
                    </div>
                    <div>
                      <Text strong>Volatility: </Text>
                      <Text style={{ color: '#cf1322' }}>
                        {(optimizationData.volatility * 100).toFixed(2)}%
                      </Text>
                    </div>
                    <div>
                      <Text strong>Sharpe Ratio: </Text>
                      <Text style={{ color: '#1890ff' }}>
                        {optimizationData.sharpe_ratio.toFixed(3)}
                      </Text>
                    </div>
                    <div>
                      <Text strong>Optimization Time: </Text>
                      <Text>{optimizationData.optimization_time.toFixed(3)}s</Text>
                    </div>
                  </Space>
                </Card>
              </Col>
            </Row>

            <Card title="Portfolio Weights" size="small">
              <Table
                columns={columns}
                dataSource={dataSource}
                pagination={false}
                size="small"
              />
            </Card>
          </>
        )}
      </Space>
    </OptimizerContainer>
  );
};

export default PortfolioOptimizer;
