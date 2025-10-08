import React, { useState } from 'react';
import { Card, Input, Button, Space, Typography, Spin, message, Tag, Row, Col } from 'antd';
import { HeartOutlined, SendOutlined } from '@ant-design/icons';
import { useQuery } from 'react-query';
import axios from 'axios';
import styled from 'styled-components';

const { Title, Text } = Typography;
const { TextArea } = Input;

const SentimentContainer = styled.div`
  .sentiment-card {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
`;

const SentimentGauge = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  background: linear-gradient(90deg, #ff4d4f 0%, #faad14 50%, #52c41a 100%);
  border-radius: 50%;
  position: relative;
  margin: 20px 0;
  
  .gauge-content {
    background: white;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
`;

const fetchSentimentAnalysis = async (text) => {
  const response = await axios.post('/api/sentiment', {
    text
  });
  return response.data;
};

const fetchBatchSentiment = async (texts) => {
  const response = await axios.post('/api/sentiment/batch', {
    texts
  });
  return response.data;
};

const SentimentAnalysis = () => {
  const [text, setText] = useState('Apple\'s quarterly earnings exceeded expectations with strong iPhone sales');
  const [batchTexts, setBatchTexts] = useState([
    'The market is showing strong bullish momentum',
    'Investors are concerned about the economic outlook',
    'Company earnings beat expectations significantly',
    'Stock prices remain volatile amid uncertainty'
  ]);

  const { data: sentimentData, isLoading, refetch } = useQuery(
    ['sentimentAnalysis', text],
    () => fetchSentimentAnalysis(text),
    {
      enabled: false,
      onError: (error) => {
        message.error('Failed to analyze sentiment');
      }
    }
  );

  const { data: batchData, isLoading: batchLoading, refetch: refetchBatch } = useQuery(
    ['batchSentimentAnalysis', batchTexts],
    () => fetchBatchSentiment(batchTexts),
    {
      enabled: false,
      onError: (error) => {
        message.error('Failed to analyze batch sentiment');
      }
    }
  );

  const handleAnalyze = () => {
    refetch();
  };

  const handleBatchAnalyze = () => {
    refetchBatch();
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return '#52c41a';
      case 'negative': return '#ff4d4f';
      default: return '#faad14';
    }
  };

  const getSentimentTag = (sentiment) => {
    const color = getSentimentColor(sentiment);
    return <Tag color={color}>{sentiment.toUpperCase()}</Tag>;
  };

  const getPolarityColor = (polarity) => {
    if (polarity > 0.1) return '#52c41a';
    if (polarity < -0.1) return '#ff4d4f';
    return '#faad14';
  };

  return (
    <SentimentContainer>
      <Space direction="vertical" size="large" style={{ width: '100%' }}>
        <div>
          <Title level={2}>😊 Sentiment Analysis</Title>
          <Text type="secondary">
            Analyze financial text sentiment using advanced NLP techniques
          </Text>
        </div>

        <Card title="Single Text Analysis" size="small" className="sentiment-card">
          <Space direction="vertical" style={{ width: '100%' }}>
            <TextArea
              placeholder="Enter financial text to analyze..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={4}
            />
            <Button
              type="primary"
              icon={<HeartOutlined />}
              onClick={handleAnalyze}
              loading={isLoading}
            >
              Analyze Sentiment
            </Button>
          </Space>
        </Card>

        {isLoading && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>Analyzing sentiment...</Text>
            </div>
          </div>
        )}

        {sentimentData && !isLoading && (
          <Card title="Analysis Results" size="small" className="sentiment-card">
            <Row gutter={[16, 16]}>
              <Col xs={24} md={12}>
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div>
                    <Text strong>Sentiment: </Text>
                    {getSentimentTag(sentimentData.sentiment)}
                  </div>
                  <div>
                    <Text strong>Polarity: </Text>
                    <Text style={{ color: getPolarityColor(sentimentData.polarity) }}>
                      {sentimentData.polarity.toFixed(3)}
                    </Text>
                  </div>
                  <div>
                    <Text strong>Confidence: </Text>
                    <Text>{sentimentData.confidence.toFixed(3)}</Text>
                  </div>
                  <div>
                    <Text strong>Compound Score: </Text>
                    <Text>{sentimentData.compound_score.toFixed(3)}</Text>
                  </div>
                </Space>
              </Col>
              <Col xs={24} md={12}>
                <SentimentGauge>
                  <div className="gauge-content">
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: getPolarityColor(sentimentData.polarity) }}>
                      {sentimentData.polarity.toFixed(2)}
                    </div>
                    <div style={{ fontSize: '12px', color: '#666' }}>
                      Polarity
                    </div>
                  </div>
                </SentimentGauge>
              </Col>
            </Row>
          </Card>
        )}

        <Card title="Batch Analysis" size="small" className="sentiment-card">
          <Space direction="vertical" style={{ width: '100%' }}>
            <TextArea
              placeholder="Enter multiple texts separated by newlines..."
              value={batchTexts.join('\n')}
              onChange={(e) => setBatchTexts(e.target.value.split('\n').filter(t => t.trim()))}
              rows={6}
            />
            <Button
              type="default"
              icon={<SendOutlined />}
              onClick={handleBatchAnalyze}
              loading={batchLoading}
            >
              Analyze Batch
            </Button>
          </Space>
        </Card>

        {batchLoading && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin size="large" />
            <div style={{ marginTop: 16 }}>
              <Text>Analyzing batch sentiment...</Text>
            </div>
          </div>
        )}

        {batchData && !batchLoading && (
          <>
            <Card title="Batch Results" size="small" className="sentiment-card">
              <Space direction="vertical" style={{ width: '100%' }}>
                {batchData.results.map((result, index) => (
                  <div key={index} style={{ padding: '12px', border: '1px solid #f0f0f0', borderRadius: '6px', marginBottom: '8px' }}>
                    <div style={{ marginBottom: '8px' }}>
                      <Text strong>Text {index + 1}: </Text>
                      <Text>{result.text}</Text>
                    </div>
                    <Space>
                      <Text>Sentiment: </Text>
                      {getSentimentTag(result.sentiment)}
                      <Text>Polarity: </Text>
                      <Text style={{ color: getPolarityColor(result.polarity) }}>
                        {result.polarity.toFixed(3)}
                      </Text>
                      <Text>Confidence: </Text>
                      <Text>{result.confidence.toFixed(3)}</Text>
                    </Space>
                  </div>
                ))}
              </Space>
            </Card>

            <Card title="Summary Statistics" size="small" className="sentiment-card">
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
                      {batchData.summary.avg_polarity.toFixed(3)}
                    </div>
                    <Text type="secondary">Avg Polarity</Text>
                  </div>
                </Col>
                <Col xs={24} sm={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
                      {(batchData.summary.positive_ratio * 100).toFixed(1)}%
                    </div>
                    <Text type="secondary">Positive</Text>
                  </div>
                </Col>
                <Col xs={24} sm={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ff4d4f' }}>
                      {(batchData.summary.negative_ratio * 100).toFixed(1)}%
                    </div>
                    <Text type="secondary">Negative</Text>
                  </div>
                </Col>
                <Col xs={24} sm={6}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#faad14' }}>
                      {(batchData.summary.avg_confidence * 100).toFixed(1)}%
                    </div>
                    <Text type="secondary">Avg Confidence</Text>
                  </div>
                </Col>
              </Row>
            </Card>
          </>
        )}
      </Space>
    </SentimentContainer>
  );
};

export default SentimentAnalysis;
