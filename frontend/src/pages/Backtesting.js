import React, { useState } from 'react';
import { Card, Row, Col, Input, Button, Select, Space, Typography, Spin, message, Table, Statistic } from 'antd';
import { ExperimentOutlined, LineChartOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import axios from 'axios';
import Plot from 'react-plotly.js';
import styled from 'styled-components';

const { Title, Text } = Typography;
const { Option } = Select;

const BacktestingContainer = styled.div`
  .backtest-card {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
`;

const fetchBacktest = async (symbol, strategy, startDate, endDate, initialCash) => {
  const response = await axios.post('/api/backtest', {
    symbol,
    strategy,
    start_date: startDate,
    end_date: endDate,
    initial_cash: initialCash
  });
  return response.data;
};

const Backtesting = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [strategy, setStrategy] = useState('moving_average');
  const [startDate, setStartDate] = useState('2023-01-01');
  const [endDate, setEndDate] = useState('2023-12-31');
  const [initialCash, setInitialCash] = useState(100000);

  const { data: backtestData, isLoading, refetch } = useQuery(
    ['backtest', symbol, strategy, startDate, endDate, initialCash],
    () => fetchBacktest(symbol, strategy, startDate, endDate, initialCash),
    {
      enabled: false,
      onError: (error) => {
        message.error('Failed to run backtest');
      }
    }
  );

  const handleBacktest = () => {
    refetch();
  };

  const createEquityCurve = (trades) => {
    if (!trades || trades.length === 0) return null;

    // Generate mock equity curve data
    const dates = [];
    const equity = [];
    let currentEquity = initialCash;
    
    for (let i = 0; i < 252; i++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + i);
      dates.push(date);
      
      // Simulate equity growth
      currentEquity *= (1 + (Math.random() - 0.5) * 0.02);
      equity.push(currentEquity);
    }

    return {
      data: [{
        x: dates,
        y: equity,
        type: 'scatter',
        mode: 'lines',
        name: 'Equity Curve',
        line: { color: '#1890ff', width: 2 }
      }],
      layout: {
        title: 'Equity Curve',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Portfolio Value ($)' },
        height: 400
      }
    };
  };

  const createDrawdownChart = (trades) => {
    if (!trades || trades.length === 0) return null;

    // Generate mock drawdown data
    const dates = [];
    const drawdown = [];
    
    for (let i = 0; i < 252; i++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + i);
      dates.push(date);
      
      // Simulate drawdown
      drawdown.push((Math.random() - 0.5) * 20);
    }

    return {
      data: [{
        x: dates,
        y: drawdown,
        type: 'scatter',
        mode: 'lines',
        name: 'Drawdown %',
        fill: 'tonexty',
        line: { color: '#ff4d4f' }
      }],
      layout: {
        title: 'Drawdown Analysis',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Drawdown (%)' },
        height: 300
      }
    };
  };

  const tradeColumns = [
    {
      title: 'Entry Date',
      dataIndex: 'entry_date',
      key: 'entry_date',
      render: (date) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Exit Date',
      dataIndex: 'exit_date',
      key: 'exit_date',
      render: (date) => new Date(date).toLocaleDateString(),
    },
    {
      title: 'Entry Price',
      dataIndex: 'entry_price',
      key: 'entry_price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Exit Price',
      dataIndex: 'exit_price',
      key: 'exit_price',
      render: (price) => `$${price.toFixed(2)}`,
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
    },
    {
      title: 'P&L',
      dataIndex: 'pnl',
      key: 'pnl',
      render: (pnl) => (
        <Text style={{ color: pnl >= 0 ? '#52c41a' : '#ff4d4f' }}>
          ${pnl.toFixed(2)}
        </Text>
      ),
    },
    {
      title: 'P&L %',
      dataIndex: 'pnl_pct',
      key: 'pnl_pct',
      render: (pnlPct) => (
        <Text style={{ color: pnlPct >= 0 ? '#52c41a' : '#ff4d4f' }}>
          {(pnlPct * 100).toFixed(2)}%
        </Text>
      ),
    },
    {
      title: 'Holding Period',
      dataIndex: 'holding_period',
      key: 'holding_period',
      render: (days) => `${days} days`,
    },
  ];

  return (
    <BacktestingContainer>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={2}>🧪 Strategy Backtesting</Title>
          <Text type="secondary">
            Test trading strategies with historical data and performance analysis
          </Text>
        </div>

        <Card title="Backtest Configuration" size="small" className="backtest-card">
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={6}>
              <Input
                placeholder="Symbol"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              />
            </Col>
            <Col xs={24} sm={6}>
              <Select
                value={strategy}
                onChange={setStrategy}
                style={{ width: '100%' }}
              >
                <Option value="moving_average">Moving Average</Option>
                <Option value="rsi">RSI Strategy</Option>
              </Select>
            </Col>
            <Col xs={24} sm={6}>
              <Input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </Col>
            <Col xs={24} sm={6}>
              <Input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </Col>
          </Row>
          <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
            <Col xs={24} sm={12}>
              <Input
                placeholder="Initial Cash"
                value={initialCash}
                onChange={(e) => setInitialCash(parseFloat(e.target.value) || 100000)}
                prefix="$"
              />
            </Col>
            <Col xs={24} sm={12}>
              <Button
                type="primary"
                icon={<ExperimentOutlined />}
                onClick={handleBacktest}
                loading={isLoading}
                block
              >
                Run Backtest
              </Button>
            </Col>
          </Row>
        </Card>

        {isLoading && (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>Running backtest...</Text>
            </div>
          </div>
        )}

        {backtestData && !isLoading && (
          <>
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Card title="Performance Metrics" size="small" className="backtest-card">
                  <Row gutter={[16, 16]}>
                    <Col xs={12}>
                      <Statistic
                        title="Total Return"
                        value={backtestData.total_return * 100}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: backtestData.total_return >= 0 ? '#3f8600' : '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12}>
                      <Statistic
                        title="Annualized Return"
                        value={backtestData.annualized_return * 100}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: backtestData.annualized_return >= 0 ? '#3f8600' : '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12}>
                      <Statistic
                        title="Volatility"
                        value={backtestData.volatility * 100}
                        precision={2}
                        suffix="%"
                      />
                    </Col>
                    <Col xs={12}>
                      <Statistic
                        title="Sharpe Ratio"
                        value={backtestData.sharpe_ratio}
                        precision={3}
                      />
                    </Col>
                    <Col xs={12}>
                      <Statistic
                        title="Max Drawdown"
                        value={backtestData.max_drawdown * 100}
                        precision={2}
                        suffix="%"
                        valueStyle={{ color: '#cf1322' }}
                      />
                    </Col>
                    <Col xs={12}>
                      <Statistic
                        title="Win Rate"
                        value={backtestData.win_rate * 100}
                        precision={1}
                        suffix="%"
                      />
                    </Col>
                  </Row>
                </Card>
              </Col>
              
              <Col xs={24} lg={12}>
                <Card title="Trade Statistics" size="small" className="backtest-card">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Strategy: </Text>
                      <Text>{backtestData.strategy.replace('_', ' ').toUpperCase()}</Text>
                    </div>
                    <div>
                      <Text strong>Symbol: </Text>
                      <Text>{backtestData.symbol}</Text>
                    </div>
                    <div>
                      <Text strong>Total Trades: </Text>
                      <Text>{backtestData.total_trades}</Text>
                    </div>
                    <div>
                      <Text strong>Average Trade Return: </Text>
                      <Text style={{ color: backtestData.avg_trade_return >= 0 ? '#3f8600' : '#cf1322' }}>
                        {(backtestData.avg_trade_return * 100).toFixed(2)}%
                      </Text>
                    </div>
                  </Space>
                </Card>
              </Col>
            </Row>

            <Card title="Equity Curve" size="small" className="backtest-card">
              <div style={{ height: '400px' }}>
                <Plot
                  data={createEquityCurve(backtestData.trades).data}
                  layout={createEquityCurve(backtestData.trades).layout}
                  style={{ width: '100%', height: '100%' }}
                />
              </div>
            </Card>

            <Card title="Drawdown Analysis" size="small" className="backtest-card">
              <div style={{ height: '300px' }}>
                <Plot
                  data={createDrawdownChart(backtestData.trades).data}
                  layout={createDrawdownChart(backtestData.trades).layout}
                  style={{ width: '100%', height: '100%' }}
                />
              </div>
            </Card>

            <Card title="Trade History" size="small" className="backtest-card">
              <Table
                columns={tradeColumns}
                dataSource={backtestData.trades.map((trade, index) => ({
                  ...trade,
                  key: index
                }))}
                pagination={{ pageSize: 10 }}
                size="small"
                scroll={{ x: 800 }}
              />
            </Card>
          </>
        )}
      </Space>
    </BacktestingContainer>
  );
};

export default Backtesting;
