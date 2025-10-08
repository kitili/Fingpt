import React from 'react';
import { Layout, Typography, Badge, Avatar, Dropdown, Menu } from 'antd';
import { BellOutlined, UserOutlined, SettingOutlined, LogoutOutlined } from '@ant-design/icons';
import styled from 'styled-components';

const { Header: AntHeader } = Layout;
const { Title, Text } = Typography;

const StyledHeader = styled(AntHeader)`
  background: #fff;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
`;

const HeaderLeft = styled.div`
  display: flex;
  align-items: center;
`;

const HeaderRight = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  
  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #52c41a;
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
`;

const Header = () => {
  const userMenu = (
    <Menu>
      <Menu.Item key="profile" icon={<UserOutlined />}>
        Profile
      </Menu.Item>
      <Menu.Item key="settings" icon={<SettingOutlined />}>
        Settings
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />}>
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <StyledHeader>
      <HeaderLeft>
        <Title level={3} style={{ margin: 0, color: '#1890ff' }}>
          FinGPT for Everyone
        </Title>
        <Text type="secondary" style={{ marginLeft: 16 }}>
          CS Solutions in Finance
        </Text>
      </HeaderLeft>
      
      <HeaderRight>
        <StatusIndicator>
          <div className="status-dot" />
          <Text type="secondary">API Connected</Text>
        </StatusIndicator>
        
        <Badge count={3} size="small">
          <BellOutlined style={{ fontSize: 18, color: '#666' }} />
        </Badge>
        
        <Dropdown overlay={userMenu} placement="bottomRight">
          <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
        </Dropdown>
      </HeaderRight>
    </StyledHeader>
  );
};

export default Header;
