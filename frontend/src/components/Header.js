import React, { useState, useEffect } from 'react';
import { Layout, Typography, Badge, Avatar, Dropdown, Menu, Button, message, Modal, Form, Input, Switch, Select } from 'antd';
import { BellOutlined, UserOutlined, SettingOutlined, LogoutOutlined, ClearOutlined, EditOutlined } from '@ant-design/icons';
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
  const [profileModalVisible, setProfileModalVisible] = useState(false);
  const [settingsModalVisible, setSettingsModalVisible] = useState(false);
  const [profileForm] = Form.useForm();
  const [settingsForm] = Form.useForm();
  const [userProfile, setUserProfile] = useState({
    name: 'John Doe',
    email: 'john.doe@fingpt.com',
    role: 'Financial Analyst',
    department: 'Quantitative Research',
    joinDate: '2024-01-15'
  });
  const [userSettings, setUserSettings] = useState({
    theme: 'light',
    notifications: true,
    autoRefresh: true,
    refreshInterval: 30,
    defaultPeriod: '1y',
    riskTolerance: 'moderate'
  });

  // Load saved user data on component mount
  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile');
    const savedSettings = localStorage.getItem('userSettings');
    
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile));
    }
    
    if (savedSettings) {
      setUserSettings(JSON.parse(savedSettings));
    }
  }, []);

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

  // Profile handlers
  const handleProfileClick = () => {
    setProfileModalVisible(true);
    profileForm.setFieldsValue(userProfile);
  };

  const handleProfileUpdate = async (values) => {
    try {
      const updatedProfile = { ...userProfile, ...values };
      setUserProfile(updatedProfile);
      localStorage.setItem('userProfile', JSON.stringify(updatedProfile));
      setProfileModalVisible(false);
      message.success('Profile updated successfully!');
    } catch (error) {
      message.error('Failed to update profile');
    }
  };

  // Settings handlers
  const handleSettingsClick = () => {
    setSettingsModalVisible(true);
    settingsForm.setFieldsValue(userSettings);
  };

  const handleSettingsUpdate = async (values) => {
    try {
      const updatedSettings = { ...userSettings, ...values };
      setUserSettings(updatedSettings);
      localStorage.setItem('userSettings', JSON.stringify(updatedSettings));
      setSettingsModalVisible(false);
      message.success('Settings updated successfully!');
      
      // Apply theme change if needed
      if (values.theme && values.theme !== userSettings.theme) {
        message.info('Theme change will take effect after page refresh');
      }
    } catch (error) {
      message.error('Failed to update settings');
    }
  };

  // Logout handler
  const handleLogout = () => {
    Modal.confirm({
      title: 'Confirm Logout',
      content: 'Are you sure you want to logout?',
      okText: 'Logout',
      cancelText: 'Cancel',
      onOk() {
        // Clear user data
        localStorage.removeItem('userProfile');
        localStorage.removeItem('userSettings');
        message.success('Logged out successfully!');
        
        // In a real app, you would redirect to login page
        // For now, we'll just show a message
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      },
    });
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
      <Menu.Item key="profile" icon={<UserOutlined />} onClick={handleProfileClick}>
        Profile
      </Menu.Item>
      <Menu.Item key="settings" icon={<SettingOutlined />} onClick={handleSettingsClick}>
        Settings
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
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

      {/* Profile Modal */}
      <Modal
        title="User Profile"
        open={profileModalVisible}
        onCancel={() => setProfileModalVisible(false)}
        onOk={() => profileForm.submit()}
        okText="Update Profile"
        cancelText="Cancel"
        width={600}
      >
        <Form
          form={profileForm}
          layout="vertical"
          onFinish={handleProfileUpdate}
        >
          <Form.Item
            label="Full Name"
            name="name"
            rules={[{ required: true, message: 'Please enter your name' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="Enter your full name" />
          </Form.Item>
          
          <Form.Item
            label="Email"
            name="email"
            rules={[
              { required: true, message: 'Please enter your email' },
              { type: 'email', message: 'Please enter a valid email' }
            ]}
          >
            <Input prefix={<EditOutlined />} placeholder="Enter your email" />
          </Form.Item>
          
          <Form.Item
            label="Role"
            name="role"
            rules={[{ required: true, message: 'Please enter your role' }]}
          >
            <Input placeholder="Enter your role" />
          </Form.Item>
          
          <Form.Item
            label="Department"
            name="department"
            rules={[{ required: true, message: 'Please enter your department' }]}
          >
            <Input placeholder="Enter your department" />
          </Form.Item>
          
          <Form.Item
            label="Join Date"
            name="joinDate"
          >
            <Input disabled />
          </Form.Item>
        </Form>
      </Modal>

      {/* Settings Modal */}
      <Modal
        title="Settings"
        open={settingsModalVisible}
        onCancel={() => setSettingsModalVisible(false)}
        onOk={() => settingsForm.submit()}
        okText="Save Settings"
        cancelText="Cancel"
        width={600}
      >
        <Form
          form={settingsForm}
          layout="vertical"
          onFinish={handleSettingsUpdate}
        >
          <Form.Item
            label="Theme"
            name="theme"
            tooltip="Choose your preferred theme"
          >
            <Select>
              <Select.Option value="light">Light</Select.Option>
              <Select.Option value="dark">Dark</Select.Option>
              <Select.Option value="auto">Auto (System)</Select.Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            label="Notifications"
            name="notifications"
            valuePropName="checked"
            tooltip="Enable or disable notifications"
          >
            <Switch />
          </Form.Item>
          
          <Form.Item
            label="Auto Refresh"
            name="autoRefresh"
            valuePropName="checked"
            tooltip="Automatically refresh data"
          >
            <Switch />
          </Form.Item>
          
          <Form.Item
            label="Refresh Interval (seconds)"
            name="refreshInterval"
            tooltip="How often to refresh data automatically"
          >
            <Select>
              <Select.Option value={15}>15 seconds</Select.Option>
              <Select.Option value={30}>30 seconds</Select.Option>
              <Select.Option value={60}>1 minute</Select.Option>
              <Select.Option value={300}>5 minutes</Select.Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            label="Default Analysis Period"
            name="defaultPeriod"
            tooltip="Default time period for analysis"
          >
            <Select>
              <Select.Option value="1d">1 Day</Select.Option>
              <Select.Option value="1mo">1 Month</Select.Option>
              <Select.Option value="3mo">3 Months</Select.Option>
              <Select.Option value="6mo">6 Months</Select.Option>
              <Select.Option value="1y">1 Year</Select.Option>
            </Select>
          </Form.Item>
          
          <Form.Item
            label="Risk Tolerance"
            name="riskTolerance"
            tooltip="Your risk tolerance level for portfolio optimization"
          >
            <Select>
              <Select.Option value="conservative">Conservative</Select.Option>
              <Select.Option value="moderate">Moderate</Select.Option>
              <Select.Option value="aggressive">Aggressive</Select.Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </StyledHeader>
  );
};

export default Header;
