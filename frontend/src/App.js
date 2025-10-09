import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ConfigProvider } from 'antd';
import { Layout } from 'antd';
import styled from 'styled-components';

// Components
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import MarketAnalysis from './pages/MarketAnalysis';
import PortfolioOptimizer from './pages/PortfolioOptimizer';
import SentimentAnalysis from './pages/SentimentAnalysis';
import Backtesting from './pages/Backtesting';
import TechnicalAnalysis from './pages/TechnicalAnalysis';
import RiskAnalysis from './pages/RiskAnalysis';
import About from './pages/About';

// Styled Components
const StyledLayout = styled(Layout)`
  min-height: 100vh;
  background: #f0f2f5;
`;

const ContentWrapper = styled(Layout.Content)`
  margin: 24px;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Ant Design theme
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider theme={theme}>
        <Router>
          <StyledLayout>
            <Sidebar />
            <Layout>
              <Header />
              <ContentWrapper>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/market" element={<MarketAnalysis />} />
                  <Route path="/portfolio" element={<PortfolioOptimizer />} />
                  <Route path="/sentiment" element={<SentimentAnalysis />} />
                  <Route path="/technical" element={<TechnicalAnalysis />} />
                  <Route path="/risk" element={<RiskAnalysis />} />
                  <Route path="/backtesting" element={<Backtesting />} />
                  <Route path="/about" element={<About />} />
                  <Route path="*" element={<Dashboard />} />
                </Routes>
              </ContentWrapper>
            </Layout>
          </StyledLayout>
        </Router>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;
