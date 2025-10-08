import React from 'react';
import { Row, Col, Card, Statistic, Typography, Space, Button } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, DollarOutlined, LineChartOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import axios from 'axios';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const { Title, Text } = Typography;

const DashboardContainer = styled.div`
  .metric-card {
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
`;

const MetricCard = styled(Card)`
  .ant-card-body {
    padding: 24px;
  }
`;

const fetchMarketData = async () => {
  const response = await axios.post('/api/market-data', {
    symbols: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
    period: '1d'
  });
  return response.data;
};

const Dashboard = () => {
  const { data: marketData, isLoading, error } = useQuery('marketData', fetchMarketData);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  if (isLoading) {
    return <div>Loading market data...</div>;
  }

  if (error) {
    return <div>Error loading data: {error.message}</div>;
  }

  const summary = marketData?.data?.summary || {};

  return (
    <DashboardContainer>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <Title level={2}>📊 Financial Dashboard</Title>
            <Text type="secondary">
              Real-time market analysis and portfolio insights powered by computer science
            </Text>
          </div>

          <Row gutter={[16, 16]}>
            {Object.entries(summary).map(([symbol, data]) => (
              <Col xs={24} sm={12} lg={8} xl={6} key={symbol}>
                <motion.div variants={itemVariants}>
                  <MetricCard className="metric-card">
                    <Statistic
                      title={symbol}
                      value={data.current_price}
                      precision={2}
                      prefix="$"
                      valueStyle={{ color: data.daily_change_pct >= 0 ? '#3f8600' : '#cf1322' }}
                      suffix={
                        data.daily_change_pct >= 0 ? (
                          <ArrowUpOutlined style={{ color: '#3f8600' }} />
                        ) : (
                          <ArrowDownOutlined style={{ color: '#cf1322' }} />
                        )
                      }
                    />
                    <div style={{ marginTop: 8 }}>
                      <Text type={data.daily_change_pct >= 0 ? 'success' : 'danger'}>
                        {data.daily_change_pct >= 0 ? '+' : ''}{data.daily_change_pct.toFixed(2)}%
                      </Text>
                      <Text type="secondary" style={{ marginLeft: 8 }}>
                        Vol: {data.volatility.toFixed(2)}%
                      </Text>
                    </div>
                  </MetricCard>
                </motion.div>
              </Col>
            ))}
          </Row>

          <Row gutter={[16, 16]}>
            <Col xs={24} lg={12}>
              <motion.div variants={itemVariants}>
                <Card title="🎯 Quick Actions" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <Button type="primary" icon={<LineChartOutlined />} block>
                      Analyze Market Trends
                    </Button>
                    <Button icon={<DollarOutlined />} block>
                      Optimize Portfolio
                    </Button>
                    <Button block>
                      Run Sentiment Analysis
                    </Button>
                    <Button block>
                      Backtest Strategy
                    </Button>
                  </Space>
                </Card>
              </motion.div>
            </Col>
            
            <Col xs={24} lg={12}>
              <motion.div variants={itemVariants}>
                <Card title="📈 Market Overview" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Total Symbols Analyzed: </Text>
                      <Text>{Object.keys(summary).length}</Text>
                    </div>
                    <div>
                      <Text strong>Average Volatility: </Text>
                      <Text>
                        {Object.values(summary).reduce((acc, data) => acc + data.volatility, 0) / Object.keys(summary).length}%
                      </Text>
                    </div>
                    <div>
                      <Text strong>Positive Performers: </Text>
                      <Text>
                        {Object.values(summary).filter(data => data.daily_change_pct > 0).length} / {Object.keys(summary).length}
                      </Text>
                    </div>
                  </Space>
                </Card>
              </motion.div>
            </Col>
          </Row>

          <motion.div variants={itemVariants}>
            <Card title="🚀 CS Concepts in Action" size="small">
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} md={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 24, marginBottom: 8 }}>🔍</div>
                    <Text strong>Data Structures</Text>
                    <br />
                    <Text type="secondary">Efficient data processing</Text>
                  </div>
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 24, marginBottom: 8 }}>🤖</div>
                    <Text strong>Machine Learning</Text>
                    <br />
                    <Text type="secondary">Predictive modeling</Text>
                  </div>
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 24, marginBottom: 8 }}>⚖️</div>
                    <Text strong>Optimization</Text>
                    <br />
                    <Text type="secondary">Portfolio management</Text>
                  </div>
                </Col>
                <Col xs={24} sm={12} md={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: 24, marginBottom: 8 }}>🌐</div>
                    <Text strong>Web Development</Text>
                    <br />
                    <Text type="secondary">Real-time dashboards</Text>
                  </div>
                </Col>
              </Row>
            </Card>
          </motion.div>
        </Space>
      </motion.div>
    </DashboardContainer>
  );
};

export default Dashboard;
