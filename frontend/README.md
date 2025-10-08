# FinGPT Frontend

A modern React-based frontend for the FinGPT financial analysis platform.

## Features

- 🎨 **Modern UI/UX** - Built with Ant Design and styled-components
- 📊 **Interactive Charts** - Real-time data visualization with Plotly.js
- 🔄 **Real-time Updates** - Live market data and portfolio tracking
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- ⚡ **Fast Performance** - Optimized with React Query for data fetching
- 🎭 **Smooth Animations** - Enhanced UX with Framer Motion

## Tech Stack

- **React 18** - Modern React with hooks
- **Ant Design** - Enterprise UI components
- **React Router** - Client-side routing
- **React Query** - Data fetching and caching
- **Plotly.js** - Interactive charts and graphs
- **Styled Components** - CSS-in-JS styling
- **Framer Motion** - Animation library
- **Axios** - HTTP client

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- FinGPT API server running on port 8000

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Building for Production

```bash
npm run build
# or
yarn build
```

This creates a `build` folder with optimized production files.

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Sidebar.js
│   │   └── Header.js
│   ├── pages/
│   │   ├── Dashboard.js
│   │   ├── MarketAnalysis.js
│   │   ├── PortfolioOptimizer.js
│   │   ├── SentimentAnalysis.js
│   │   ├── Backtesting.js
│   │   └── About.js
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── helpers.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## API Integration

The frontend communicates with the FinGPT API server running on port 8000. Make sure the API server is running before starting the frontend.

### API Endpoints Used

- `POST /api/market-data` - Fetch market data
- `POST /api/sentiment` - Analyze sentiment
- `POST /api/portfolio/optimize` - Optimize portfolio
- `POST /api/backtest` - Run strategy backtesting

## Features Overview

### Dashboard
- Real-time market overview
- Key performance metrics
- Quick action buttons
- CS concepts showcase

### Market Analysis
- Interactive price charts
- Technical indicators
- Volatility analysis
- Multi-symbol comparison

### Portfolio Optimizer
- Multiple optimization methods
- Risk-return visualization
- Efficient frontier plotting
- Portfolio weight allocation

### Sentiment Analysis
- Text sentiment scoring
- Batch analysis
- Confidence metrics
- Financial lexicon integration

### Strategy Backtesting
- Multiple trading strategies
- Performance metrics
- Trade history
- Risk analysis

## Customization

### Theming
The app uses Ant Design's theming system. Modify the theme in `App.js`:

```javascript
const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
  },
};
```

### Styling
Use styled-components for custom styling:

```javascript
const CustomComponent = styled.div`
  background: #fff;
  padding: 16px;
  border-radius: 8px;
`;
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
