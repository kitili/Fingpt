import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  LineChartOutlined,
  PieChartOutlined,
  HeartOutlined,
  ExperimentOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import styled from 'styled-components';

const { Sider } = Layout;

const StyledSider = styled(Sider)`
  background: #001529;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  
  .ant-layout-sider-trigger {
    background: #002140;
  }
`;

const Logo = styled.div`
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  border-bottom: 1px solid #002140;
  margin-bottom: 16px;
`;

const menuItems = [
  {
    key: '/',
    icon: <DashboardOutlined />,
    label: 'Dashboard',
  },
  {
    key: '/market',
    icon: <LineChartOutlined />,
    label: 'Market Analysis',
  },
  {
    key: '/portfolio',
    icon: <PieChartOutlined />,
    label: 'Portfolio Optimizer',
  },
  {
    key: '/sentiment',
    icon: <HeartOutlined />,
    label: 'Sentiment Analysis',
  },
  {
    key: '/backtesting',
    icon: <ExperimentOutlined />,
    label: 'Strategy Backtesting',
  },
  {
    key: '/about',
    icon: <InfoCircleOutlined />,
    label: 'About',
  },
];

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleMenuClick = ({ key }) => {
    navigate(key);
  };

  return (
    <StyledSider width={250} collapsible>
      <Logo>📊 FinGPT</Logo>
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={handleMenuClick}
      />
    </StyledSider>
  );
};

export default Sidebar;
