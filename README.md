# Crypto Risk Analyzer

A comprehensive cryptocurrency risk analysis platform that provides real-time risk scoring, volatility analysis, and investment insights for 10,000+ cryptocurrencies. The platform combines data engineering pipelines, machine learning models, and a modern web interface to deliver actionable risk metrics.

## 📋 Overview

The Crypto Risk Analyzer is a full-stack application that:

- **Extracts** real-time cryptocurrency data from multiple sources (CoinGecko, Binance)
- **Transforms** raw data into meaningful features using statistical and technical analysis
- **Loads** processed data into a structured format for analysis
- **Analyzes** risk using a proprietary scoring algorithm combining volatility, liquidity, sentiment, and momentum
- **Visualizes** insights through an interactive React-based dashboard

The system is designed with a modern data engineering architecture, featuring automated ETL pipelines orchestrated by Apache Airflow, a TypeScript/React frontend, and Python-based risk modeling.
```bash
## 🏗️ Project Structure
RiskCoin-Detected/
├── airflow/                  # Airflow DAG definitions
│   └── dags.py              # ETL pipeline orchestration
├── data/                     # Data storage
│   ├── raw/                 # Raw extracted data
│   │   ├── binance/         # Binance orderbook data
│   │   └── coingecko/       # CoinGecko market data
│   └── processed/           # Transformed and cleaned data
├── models/                   # Risk scoring models
│   └── risk_models.py       # Composite risk score computation
├── source/                   # ETL pipeline scripts
│   ├── extract_coingecko.py # CoinGecko API client
│   ├── extracts_binance.py  # Binance API client
│   ├── transform_cleaning.py# Data cleaning and validation
│   ├── features.py          # Feature engineering
│   └── loads.py             # Data loading utilities
├── src/                      # Frontend React application
│   ├── components/          # React components
│   │   ├── CoinCard.tsx     # Coin display card
│   │   ├── SearchBar.tsx    # Search functionality
│   │   ├── StabilityChart.tsx# Price chart component
│   │   ├── MetricsPanel.tsx # Risk metrics display
│   │   └── ui/              # shadcn/ui component library
│   ├── pages/               # Page components
│   │   ├── Index.tsx        # Home/landing page
│   │   ├── CoinDetail.tsx   # Individual coin detail page
│   │   └── NotFound.tsx     # 404 error page
│   ├── hooks/               # Custom React hooks
│   │   ├── use-toast.ts     # Toast notifications
│   │   └── use-mobile.tsx   # Mobile detection
│   ├── lib/                 # Utility libraries
│   │   ├── mockData.ts      # Mock data for development
│   │   └── utils.ts         # Helper functions
│   ├── types/               # TypeScript type definitions
│   │   └── crypto.ts        # Crypto data interfaces
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── .gitignore               # Git ignore rules
├── components.json          # shadcn/ui configuration
├── eslint.config.js         # ESLint configuration
├── package.json             # Node.js dependencies
├── postcss.config.js        # PostCSS configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
├── vite.config.ts           # Vite build configuration
└── README.md                # Project documentation
```
## 🛠️ Technology Stack
<img width="1024" height="1024" alt="WorkFlow" src="https://github.com/user-attachments/assets/1e281d6a-2a5f-44d9-9291-3ca137503958" />
Data Flow Architecture
```bash
┌─────────────────┐
│ External APIs │
│ (CoinGecko, │
│ Binance) │
└────────┬────────┘
│
▼
┌─────────────────┐
│ Airflow DAGs │ ◄─── Orchestrates ETL pipeline
│ (dags.py) │ Runs every 6 hours
└────────┬────────┘
│
▼
┌─────────────────┐
│ Extract Layer │ ◄─── Python scripts fetch raw data
│ (source/.py) │ Stores in data/raw/
└────────┬────────┘
│
▼
┌─────────────────┐
│ Transform Layer │ ◄─── Cleans, validates, engineers features
│ (features.py, │ Computes rolling statistics
│ transform_) │
└────────┬────────┘
│
▼
┌─────────────────┐
│ Risk Models │ ◄─── Computes composite risk scores
│ (risk_models.py)│ Weighted combination of metrics
└────────┬────────┘
│
▼
┌─────────────────┐
│ Processed Data │ ◄─── Structured data ready for consumption
│ (data/processed)│
└────────┬────────┘
│
▼
┌─────────────────┐
│ React Frontend │ ◄─── TypeScript/React displays data
│ (src/) │ TanStack Query manages state
└─────────────────┘

```


## Component Interaction. 
<img width="1536" height="1024" alt="Data Architecture" src="https://github.com/user-attachments/assets/650f0c56-8c33-4284-b59c-371dbe26d4a5" />
## Score Criteria
- **Default Weights:
- **Volatility: 35%
- **Liquidity: 25%
- **Sentiment: 20%
- **Momentum: 20%
- **Score Range: 0-100 (lower = lower risk)
## Project Components
<img width="1024" height="1024" alt="Project Component" src="https://github.com/user-attachments/assets/fde7837e-780d-4162-8f50-8fae3a009b7c" />

🔄 CI/CD Pipeline
Current Setup
The project currently uses:
Git for version control
npm scripts for build automation:
npm run dev - Development server
npm run build - Production build
npm run lint - Code linting
npm run preview - Preview production build
Recommended CI/CD Setup
For production deployment, consider implementing:
GitHub Actions Workflow
# .github/workflows/ci.ymlname: CI/CD Pipelineon:  push:    branches: [main, develop]  pull_request:    branches: [main]jobs:  lint:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-node@v3        with:          node-version: '18'      - run: npm ci      - run: npm run lint  build:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-node@v3        with:          node-version: '18'      - run: npm ci      - run: npm run build      - uses: actions/upload-artifact@v3        with:          name: dist          path: dist/  test:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-python@v4        with:          python-version: '3.9'      - run: pip install -r requirements.txt      - run: pytest  # If tests are added
Deployment Options
Frontend: Vercel, Netlify, or AWS S3 + CloudFront
Backend/API: AWS Lambda, Google Cloud Functions, or containerized deployment
Airflow: Managed service (Astronomer, Google Composer) or self-hosted
📐 Data Modeling Approach
Type Definitions (TypeScript)
The frontend uses TypeScript interfaces to ensure type safety:
}
interface Coin {  id: string;  symbol: string;  name: string;  current_price: number;  price_change_24h: number;  price_change_percentage_24h: number;  market_cap: number;  total_volume: number;  rank: number;  risk_score: number;  volatility_score: number;  liquidity_score: number;  sentiment_score: number;  image?: string;}interface CoinDetail extends Coin {  market_cap_rank: number;  ath: number;  ath_change_percentage: number;  atl: number;  atl_change_percentage: number;  circulating_supply: number;  max_supply: number;  description?: string;}interface PricePoint {  timestamp: number;  price: number;  volume: number;  volatility?: number;  ma_7?: number;  ma_30?: number;}
Feature Engineering
Features are computed using rolling windows and technical indicators:
Rolling Statistics:
Moving averages (7, 14, 30 day)
Standard deviation (volatility)
Min/max values
Returns (percentage change)
Technical Indicators:
RSI (Relative Strength Index)
Momentum indicators
Price distance from moving averages
Derived Metrics:
Volatility score (normalized 0-100)
Liquidity score (based on volume and orderbook depth)
Sentiment score (from external APIs or social media)
Risk score (weighted composite)
Data Normalization
All scores are normalized to a 0-100 scale for consistency:
Lower scores = Lower risk / Better metrics
Higher scores = Higher risk / Worse metrics
🚀 User Setup
Prerequisites
Node.js 18+ and npm
Python 3.9+
Apache Airflow (for ETL pipeline)
Git
Frontend Setup
Clone the repository:
   git clone <repository-url>   cd RiskCoin-Detected
Install dependencies:
   npm install
Start development server:
   npm run dev
Access the application:
Open http://localhost:8080 in your browser
Backend/Data Pipeline Setup
Create Python virtual environment:
   python3 -m venv venv   source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Python dependencies:
   pip install pandas numpy requests apache-airflow
Configure Airflow:
   # Initialize Airflow database   airflow db init      # Create admin user   airflow users create \     --username admin \     --firstname Admin \     --lastname User \     --role Admin \     --email admin@example.com      # Start Airflow webserver   airflow webserver --port 8080      # Start Airflow scheduler (in another terminal)   airflow scheduler
Update DAG paths (if needed):
Edit airflow/dags.py to match your project path
Ensure source/ directory is in Python path
Run ETL pipeline manually (optional):
   python -m source.extract_coingecko   python -m source.extracts_binance
Environment Variables
Create a .env file in the project root (optional):
# CoinGecko API (optional, for higher rate limits)COINGECKO_API_KEY=your_api_key_here# Binance API (optional)BINANCE_API_KEY=your_api_key_hereBINANCE_SECRET_KEY=your_secret_key_here
Build for Production
# Build frontendnpm run build# Output will be in dist/ directory# Deploy dist/ to your hosting service
Troubleshooting
Port already in use:
Change port in vite.config.ts or kill process using port 8080
Module not found errors:
Run npm install again
Check that all dependencies are in package.json
Airflow DAG not showing:
Check DAG file syntax
Verify Python path includes project root
Check Airflow logs for errors
TypeScript errors:
Run npm run lint to see detailed errors
Ensure all imports are correct
📝 Development Notes
The frontend currently uses mock data (src/lib/mockData.ts) for development
To connect to real data, implement API endpoints and update TanStack Query hooks
Airflow DAGs run every 6 hours by default (configurable in dags.py)
Risk score weights can be adjusted in models/risk_models.py
