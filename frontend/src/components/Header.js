import React, { useState, useEffect } from 'react';
import { Layout, Typography, Badge, Avatar, Dropdown, Menu, Button, message } from 'antd';
import { BellOutlined, UserOutlined, SettingOutlined, LogoutOutlined, ClearOutlined } from '@ant-design/icons';
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
  const [notifications, setNotifications] = useState([]);
  const [apiStatus, setApiStatus] = useState('checking');

  // Check API status and generate notifications
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
          setApiStatus('connected');
          // Generate sample notifications
          const sampleNotifications = [
            {
              id: 1,
              title: 'Portfolio Optimization Complete',
              message: 'Your portfolio has been optimized with a Sharpe ratio of 1.23',
              time: '2 minutes ago',
              type: 'success'
            },
            {
              id: 2,
              title: 'Market Alert',
              message: 'AAPL price has increased by 5.2% today',
              time: '15 minutes ago',
              type: 'info'
            },
            {
              id: 3,
              title: 'Risk Analysis Warning',
              message: 'Portfolio volatility has exceeded 15% threshold',
              time: '1 hour ago',
              type: 'warning'
            }
          ];
          setNotifications(sampleNotifications);
        } else {
          setApiStatus('disconnected');
        }
      } catch (error) {
        setApiStatus('disconnected');
        console.error('API check failed:', error);
      }
    };

    checkApiStatus();
    // Check every 30 seconds
    const interval = setInterval(checkApiStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const clearAllNotifications = () => {
    setNotifications([]);
    message.success('All notifications cleared');
  };

  const notificationMenu = (
    <Menu style={{ width: 350, maxHeight: 400, overflow: 'auto' }}>
      <Menu.Item key="header" style={{ borderBottom: '1px solid #f0f0f0' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Text strong>Notifications</Text>
          {notifications.length > 0 && (
            <Button 
              type="text" 
              size="small" 
              icon={<ClearOutlined />} 
              onClick={clearAllNotifications}
            >
              Clear All
            </Button>
          )}
        </div>
      </Menu.Item>
      {notifications.length === 0 ? (
        <Menu.Item key="empty" disabled>
          <Text type="secondary">No notifications</Text>
        </Menu.Item>
      ) : (
        notifications.map(notification => (
          <Menu.Item key={notification.id} style={{ padding: '8px 16px' }}>
            <div>
              <Text strong style={{ color: notification.type === 'warning' ? '#fa8c16' : 
                    notification.type === 'success' ? '#52c41a' : '#1890ff' }}>
                {notification.title}
              </Text>
              <br />
              <Text type="secondary" style={{ fontSize: '12px' }}>
                {notification.message}
              </Text>
              <br />
              <Text type="secondary" style={{ fontSize: '11px' }}>
                {notification.time}
              </Text>
            </div>
          </Menu.Item>
        ))
      )}
    </Menu>
  );

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
          <div className="status-dot" style={{ 
            background: apiStatus === 'connected' ? '#52c41a' : 
                       apiStatus === 'disconnected' ? '#ff4d4f' : '#faad14' 
          }} />
          <Text type="secondary">
            API {apiStatus === 'connected' ? 'Connected' : 
                 apiStatus === 'disconnected' ? 'Disconnected' : 'Checking...'}
          </Text>
        </StatusIndicator>
        
        <Dropdown overlay={notificationMenu} placement="bottomRight" trigger={['click']}>
          <Badge count={notifications.length} size="small">
            <BellOutlined style={{ fontSize: 18, color: '#666', cursor: 'pointer' }} />
          </Badge>
        </Dropdown>
        
        <Dropdown overlay={userMenu} placement="bottomRight">
          <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
        </Dropdown>
      </HeaderRight>
    </StyledHeader>
  );
};

export default Header;
