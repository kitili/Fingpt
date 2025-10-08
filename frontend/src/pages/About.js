import React from 'react';
import { Card, Row, Col, Typography, Space, Divider, Timeline, Tag } from 'antd';
import { 
  DatabaseOutlined, 
  RobotOutlined, 
  LineChartOutlined,
  ApiOutlined,
  ExperimentOutlined,
  TrophyOutlined
} from '@ant-design/icons';
import styled from 'styled-components';

const { Title, Text, Paragraph } = Typography;

const AboutContainer = styled.div`
  .feature-card {
    transition: all 0.3s ease;
    height: 100%;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
  }
  
  .icon-large {
    font-size: 48px;
    margin-bottom: 16px;
    display: block;
  }
  
  .tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
  }
`;

const About = () => {
  const csConcepts = [
    {
      title: 'Data Structures & Algorithms',
      description: 'Efficient data processing, sorting, searching, and optimization algorithms for financial data analysis.',
      icon: <DatabaseOutlined className="icon-large" style={{ color: '#1890ff' }} />,
      examples: ['Hash tables for O(1) lookups', 'Graph algorithms for portfolio optimization', 'Sorting algorithms for data analysis']
    },
    {
      title: 'Machine Learning & AI',
      description: 'Predictive modeling, classification, and natural language processing for financial insights.',
      icon: <RobotOutlined className="icon-large" style={{ color: '#52c41a' }} />,
      examples: ['Sentiment analysis with NLP', 'Price prediction models', 'Pattern recognition in trading']
    },
    {
      title: 'Optimization & Mathematical Programming',
      description: 'Convex optimization, linear programming, and Monte Carlo methods for portfolio management.',
      icon: <LineChartOutlined className="icon-large" style={{ color: '#faad14' }} />,
      examples: ['Portfolio optimization', 'Risk management algorithms', 'Monte Carlo simulations']
    },
    {
      title: 'Web Development & APIs',
      description: 'RESTful API design, real-time dashboards, and interactive data visualization.',
      icon: <ApiOutlined className="icon-large" style={{ color: '#722ed1' }} />,
      examples: ['React frontend', 'FastAPI backend', 'Real-time data streaming']
    }
  ];

  const features = [
    {
      title: 'Market Data Analysis',
      description: 'Real-time data collection, technical indicators, and statistical analysis using pandas and numpy.',
      icon: <LineChartOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
    },
    {
      title: 'Sentiment Analysis',
      description: 'NLP techniques for analyzing financial news, social media, and market sentiment.',
      icon: <RobotOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
    },
    {
      title: 'Portfolio Optimization',
      description: 'Multiple optimization algorithms including Max Sharpe, Min Variance, and Risk Parity.',
      icon: <TrophyOutlined style={{ fontSize: '24px', color: '#faad14' }} />
    },
    {
      title: 'Strategy Backtesting',
      description: 'Comprehensive backtesting framework for testing trading strategies with historical data.',
      icon: <ExperimentOutlined style={{ fontSize: '24px', color: '#ff4d4f' }} />
    }
  ];

  const techStack = [
    'Python', 'React', 'FastAPI', 'Streamlit', 'Pandas', 'NumPy', 
    'Scikit-learn', 'Plotly', 'Ant Design', 'yfinance', 'CVXPY'
  ];

  return (
    <AboutContainer>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <Title level={1} style={{ color: '#1890ff', marginBottom: '16px' }}>
            📊 FinGPT for Everyone
          </Title>
          <Title level={3} type="secondary">
            CS Solutions in Finance
          </Title>
          <Paragraph style={{ fontSize: '16px', maxWidth: '800px', margin: '0 auto' }}>
            A comprehensive project demonstrating how computer science expertise can be applied 
            to solve real-world financial problems using AI, machine learning, and data science techniques.
          </Paragraph>
        </div>

        <Card title="🎯 Mission Statement" size="small">
          <Paragraph>
            FinGPT for Everyone bridges the gap between computer science theory and practical financial applications. 
            This project showcases how CS concepts like algorithms, data structures, machine learning, and web development 
            can be directly applied to create sophisticated financial analysis tools that provide real value to users.
          </Paragraph>
        </Card>

        <div>
          <Title level={2}>🔧 Computer Science Concepts Applied</Title>
          <Row gutter={[24, 24]}>
            {csConcepts.map((concept, index) => (
              <Col xs={24} lg={12} key={index}>
                <Card className="feature-card" size="small">
                  <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                    {concept.icon}
                    <Title level={4}>{concept.title}</Title>
                  </div>
                  <Paragraph>{concept.description}</Paragraph>
                  <ul>
                    {concept.examples.map((example, i) => (
                      <li key={i}><Text type="secondary">{example}</Text></li>
                    ))}
                  </ul>
                </Card>
              </Col>
            ))}
          </Row>
        </div>

        <div>
          <Title level={2}>🚀 Key Features</Title>
          <Row gutter={[16, 16]}>
            {features.map((feature, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <Card className="feature-card" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ textAlign: 'center' }}>
                      {feature.icon}
                      <Title level={5} style={{ marginTop: '8px' }}>{feature.title}</Title>
                    </div>
                    <Text type="secondary">{feature.description}</Text>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </div>

        <Card title="🛠️ Technology Stack" size="small">
          <div className="tech-stack">
            {techStack.map((tech, index) => (
              <Tag key={index} color="blue" style={{ fontSize: '14px', padding: '4px 12px' }}>
                {tech}
              </Tag>
            ))}
          </div>
        </Card>

        <Card title="📈 Financial Applications" size="small">
          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Title level={4}>Individual Investors</Title>
              <ul>
                <li>Personal portfolio management</li>
                <li>Risk assessment and analysis</li>
                <li>Market trend analysis</li>
                <li>Investment decision support</li>
              </ul>
            </Col>
            <Col xs={24} md={8}>
              <Title level={4}>Financial Advisors</Title>
              <ul>
                <li>Client portfolio optimization</li>
                <li>Risk management tools</li>
                <li>Performance analytics</li>
                <li>Client reporting automation</li>
              </ul>
            </Col>
            <Col xs={24} md={8}>
              <Title level={4}>Trading Firms</Title>
              <ul>
                <li>Algorithm development</li>
                <li>Strategy backtesting</li>
                <li>Risk modeling</li>
                <li>Performance optimization</li>
              </ul>
            </Col>
          </Row>
        </Card>

        <Card title="🎓 Educational Value" size="small">
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <Title level={4}>For CS Students</Title>
              <ul>
                <li>Real-world application of CS concepts</li>
                <li>Hands-on experience with modern technologies</li>
                <li>Understanding of financial domain problems</li>
                <li>Portfolio project for job applications</li>
              </ul>
            </Col>
            <Col xs={24} md={12}>
              <Title level={4}>For Finance Professionals</Title>
              <ul>
                <li>Technology solutions for financial problems</li>
                <li>Understanding of algorithmic approaches</li>
                <li>Integration of CS tools in finance</li>
                <li>Digital transformation insights</li>
              </ul>
            </Col>
          </Row>
        </Card>

        <Card title="🏆 Project Highlights" size="small">
          <Timeline
            items={[
              {
                children: (
                  <div>
                    <Title level={5}>Comprehensive Architecture</Title>
                    <Text>Modular design with separate components for data collection, analysis, optimization, and visualization.</Text>
                  </div>
                ),
              },
              {
                children: (
                  <div>
                    <Title level={5}>Multiple Frontend Options</Title>
                    <Text>Both Streamlit dashboard and React frontend for different use cases and preferences.</Text>
                  </div>
                ),
              },
              {
                children: (
                  <div>
                    <Title level={5}>RESTful API</Title>
                    <Text>Complete API with FastAPI for programmatic access and integration with other systems.</Text>
                  </div>
                ),
              },
              {
                children: (
                  <div>
                    <Title level={5}>Production Ready</Title>
                    <Text>Comprehensive testing, error handling, logging, and configuration management.</Text>
                  </div>
                ),
              },
            ]}
          />
        </Card>

        <Card title="💡 Getting Started" size="small">
          <Row gutter={[16, 16]}>
            <Col xs={24} md={8}>
              <Title level={4}>Quick Start</Title>
              <Paragraph>
                <Text code>python run_dashboard.py</Text>
                <br />
                Access at http://localhost:8501
              </Paragraph>
            </Col>
            <Col xs={24} md={8}>
              <Title level={4}>Full Stack</Title>
              <Paragraph>
                <Text code>python run_api.py</Text>
                <br />
                <Text code>python run_frontend.py</Text>
              </Paragraph>
            </Col>
            <Col xs={24} md={8}>
              <Title level={4}>Development</Title>
              <Paragraph>
                <Text code>pytest tests/</Text>
                <br />
                Run comprehensive test suite
              </Paragraph>
            </Col>
          </Row>
        </Card>

        <Divider />

        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Title level={3} style={{ color: '#1890ff' }}>
            🚀 Built with Computer Science Principles
          </Title>
          <Paragraph style={{ fontSize: '16px', color: '#666' }}>
            This project demonstrates how CS skills can be directly applied in the financial sector, 
            creating value through technology and innovation.
          </Paragraph>
        </div>
      </Space>
    </AboutContainer>
  );
};

export default About;
