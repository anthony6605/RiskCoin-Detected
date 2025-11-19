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

## 🏗️ Project Structure
RiskCoin-Detected/
├── airflow/ # Airflow DAG definitions
│ └── dags.py # ETL pipeline orchestration
├── data/ # Data storage
│ ├── raw/ # Raw extracted data
│ │ ├── binance/ # Binance orderbook data
│ │ └── coingecko/ # CoinGecko market data
│ └── processed/ # Transformed and cleaned data
├── models/ # Risk scoring models
│ └── risk_models.py # Composite risk score computation
├── source/ # ETL pipeline scripts
│ ├── extract_coingecko.py # CoinGecko API client
│ ├── extracts_binance.py # Binance API client
│ ├── transform_cleaning.py # Data cleaning and validation
│ ├── features.py # Feature engineering
│ └── loads.py # Data loading utilities
├── src/ # Frontend React application
│ ├── components/ # React components
│ │ ├── CoinCard.tsx # Coin display card
│ │ ├── SearchBar.tsx # Search functionality
│ │ ├── StabilityChart.tsx # Price chart component
│ │ ├── MetricsPanel.tsx # Risk metrics display
│ │ └── ui/ # shadcn/ui component library
│ ├── pages/ # Page components
│ │ ├── Index.tsx # Home/landing page
│ │ ├── CoinDetail.tsx # Individual coin detail page
│ │ └── NotFound.tsx # 404 error page
│ ├── hooks/ # Custom React hooks
│ │ ├── use-toast.ts # Toast notifications
│ │ └── use-mobile.tsx # Mobile detection
│ ├── lib/ # Utility libraries
│ │ ├── mockData.ts # Mock data for development
│ │ └── utils.ts # Helper functions
│ ├── types/ # TypeScript type definitions
│ │ └── crypto.ts # Crypto data interfaces
│ ├── App.tsx # Main application component
│ ├── main.tsx # Application entry point
│ └── index.css # Global styles
├── .gitignore # Git ignore rules
├── components.json # shadcn/ui configuration
├── eslint.config.js # ESLint configuration
├── package.json # Node.js dependencies
├── postcss.config.js # PostCSS configuration
├── tailwind.config.ts # Tailwind CSS configuration
├── tsconfig.json # TypeScript configuration
├── vite.config.ts # Vite build configuration
└── README.md # This file
## 🛠️ Technology Stack### Frontend- **React 18.3** - UI framework- **TypeScript 5.8** - Type safety- **Vite 5.4** - Build tool and dev server- **React Router 6.30** - Client-side routing- **TanStack Query 5.83** - Data fetching and caching- **Tailwind CSS 3.4** - Utility-first CSS framework- **shadcn/ui** - Component library (Radix UI primitives)- **Recharts 2.15** - Charting library- **Lucide React** - Icon library### Backend/Data Engineering- **Python 3.9** - Data processing language- **Apache Airflow** - Workflow orchestration- **Pandas** - Data manipulation- **NumPy** - Numerical computing- **Requests** - HTTP client for API calls### Development Tools- **ESLint 9.32** - Code linting- **TypeScript ESLint** - TypeScript-specific linting- **PostCSS** - CSS processing- **Autoprefixer** - CSS vendor prefixing## 🔄 How Technologies Interact### Data Flow Architecture
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
### Component Interaction1. **Airflow → Python Scripts**: DAGs trigger extraction tasks that call Python modules2. **Python → Data Storage**: Extracted data saved as JSON files in `data/raw/`3. **Feature Engineering**: Pandas/NumPy process raw data into features4. **Risk Modeling**: Risk models consume features to generate scores5. **Frontend → Data**: React components consume processed data (currently via mockData.ts)6. **React Router**: Handles navigation between pages (Index, CoinDetail, NotFound)7. **TanStack Query**: Manages server state, caching, and data synchronization8. **Tailwind + shadcn/ui**: Provides consistent, accessible UI components## 📊 Data Architecture### Data Sources1. **CoinGecko API**   - Market data (price, volume, market cap)   - OHLCV (Open, High, Low, Close, Volume) data   - Historical price data   - Coin metadata2. **Binance API**   - Orderbook data   - Trading pairs information   - Liquidity metrics### Data Pipeline Stages#### 1. Extract (E)- **Location**: `source/extract_coingecko.py`, `source/extracts_binance.py`- **Frequency**: Every 6 hours (configurable in Airflow DAG)- **Output**: Raw JSON files in `data/raw/{source}/`- **Format**: Timestamped files (e.g., `coins_20240101_120000.json`)#### 2. Transform (T)- **Location**: `source/transform_cleaning.py`, `source/features.py`- **Processes**:  - Data validation and cleaning  - Missing value handling  - Feature engineering:    - Rolling statistics (MA, std dev, min/max)    - Technical indicators (RSI, momentum)    - Volatility calculations    - Liquidity metrics- **Output**: Cleaned DataFrames with engineered features#### 3. Load (L)- **Location**: `source/loads.py`- **Processes**:  - Data serialization  - Storage in `data/processed/`  - Format conversion for frontend consumption### Risk Score ComputationThe risk score is a weighted composite of four components:risk_score = (    volatility_weight * volatility_score +    liquidity_weight * (100 - liquidity_score) +  # Inverted    sentiment_weight * (100 - sentiment_score) +  # Inverted    momentum_weight * momentum_score)**Default Weights**:- Volatility: 35%- Liquidity: 25%- Sentiment: 20%- Momentum: 20%**Score Range**: 0-100 (lower = lower risk)## 🧩 Project Components### Frontend Components#### Pages- **`Index.tsx`**: Landing page displaying top 20 coins, search bar, and feature highlights- **`CoinDetail.tsx`**: Individual coin analysis page with detailed metrics, charts, and risk breakdown- **`NotFound.tsx`**: 404 error page#### Reusable Components- **`CoinCard.tsx`**: Displays coin information in a card format with risk score, price, and metrics- **`SearchBar.tsx`**: Search functionality with autocomplete suggestions- **`StabilityChart.tsx`**: Interactive price chart with moving averages and volatility bands- **`MetricsPanel.tsx`**: Displays risk score, volatility, liquidity, and sentiment metrics#### UI Components (`src/components/ui/`)- Built on Radix UI primitives- Fully accessible and customizable- Includes: buttons, cards, dialogs, forms, charts, and more### Backend Components#### ETL Pipeline- **`extract_coingecko.py`**: CoinGecko API client with rate limiting and error handling- **`extracts_binance.py`**: Binance API client for orderbook data- **`transform_cleaning.py`**: Data validation and cleaning utilities- **`features.py`**: Feature engineering functions (rolling stats, technical indicators)- **`loads.py`**: Data serialization and storage utilities#### Risk Modeling- **`risk_models.py`**: Composite risk score computation with configurable weights#### Orchestration- **`airflow/dags.py`**: Airflow DAG definition for automated ETL pipeline execution## 🔄 CI/CD Pipeline### Current SetupThe project currently uses:- **Git** for version control- **npm scripts** for build automation:  - `npm run dev` - Development server  - `npm run build` - Production build  - `npm run lint` - Code linting  - `npm run preview` - Preview production build### Recommended CI/CD SetupFor production deployment, consider implementing:#### GitHub Actions Workflow# .github/workflows/ci.ymlname: CI/CD Pipelineon:  push:    branches: [main, develop]  pull_request:    branches: [main]jobs:  lint:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-node@v3        with:          node-version: '18'      - run: npm ci      - run: npm run lint  build:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-node@v3        with:          node-version: '18'      - run: npm ci      - run: npm run build      - uses: actions/upload-artifact@v3        with:          name: dist          path: dist/  test:    runs-on: ubuntu-latest    steps:      - uses: actions/checkout@v3      - uses: actions/setup-python@v4        with:          python-version: '3.9'      - run: pip install -r requirements.txt      - run: pytest  # If tests are added#### Deployment Options- **Frontend**: Vercel, Netlify, or AWS S3 + CloudFront- **Backend/API**: AWS Lambda, Google Cloud Functions, or containerized deployment- **Airflow**: Managed service (Astronomer, Google Composer) or self-hosted## 📐 Data Modeling Approach### Type Definitions (TypeScript)The frontend uses TypeScript interfaces to ensure type safety:interface Coin {  id: string;  symbol: string;  name: string;  current_price: number;  price_change_24h: number;  price_change_percentage_24h: number;  market_cap: number;  total_volume: number;  rank: number;  risk_score: number;  volatility_score: number;  liquidity_score: number;  sentiment_score: number;  image?: string;}interface CoinDetail extends Coin {  market_cap_rank: number;  ath: number;  ath_change_percentage: number;  atl: number;  atl_change_percentage: number;  circulating_supply: number;  max_supply: number;  description?: string;}interface PricePoint {  timestamp: number;  price: number;  volume: number;  volatility?: number;  ma_7?: number;  ma_30?: number;}### Feature EngineeringFeatures are computed using rolling windows and technical indicators:1. **Rolling Statistics**:   - Moving averages (7, 14, 30 day)   - Standard deviation (volatility)   - Min/max values   - Returns (percentage change)2. **Technical Indicators**:   - RSI (Relative Strength Index)   - Momentum indicators   - Price distance from moving averages3. **Derived Metrics**:   - Volatility score (normalized 0-100)   - Liquidity score (based on volume and orderbook depth)   - Sentiment score (from external APIs or social media)   - Risk score (weighted composite)### Data NormalizationAll scores are normalized to a 0-100 scale for consistency:- **Lower scores** = Lower risk / Better metrics- **Higher scores** = Higher risk / Worse metrics## 🚀 User Setup### Prerequisites- **Node.js** 18+ and npm- **Python** 3.9+- **Apache Airflow** (for ETL pipeline)- **Git**### Frontend Setup1. **Clone the repository**:      git clone <repository-url>   cd RiskCoin-Detected   2. **Install dependencies**:   npm install   3. **Start development server**:   npm run dev   4. **Access the application**:   - Open `http://localhost:8080` in your browser### Backend/Data Pipeline Setup1. **Create Python virtual environment**:     python3 -m venv venv   source venv/bin/activate  # On Windows: venv\Scripts\activate   2. **Install Python dependencies**:     pip install pandas numpy requests apache-airflow   3. **Configure Airflow**:   # Initialize Airflow database   airflow db init      # Create admin user   airflow users create \     --username admin \     --firstname Admin \     --lastname User \     --role Admin \     --email admin@example.com      # Start Airflow webserver   airflow webserver --port 8080      # Start Airflow scheduler (in another terminal)   airflow scheduler   4. **Update DAG paths** (if needed):   - Edit `airflow/dags.py` to match your project path   - Ensure `source/` directory is in Python path5. **Run ETL pipeline manually** (optional):   python -m source.extract_coingecko   python -m source.extracts_binance   ### Environment VariablesCreate a `.env` file in the project root (optional):# CoinGecko API (optional, for higher rate limits)COINGECKO_API_KEY=your_api_key_here# Binance API (optional)BINANCE_API_KEY=your_api_key_hereBINANCE_SECRET_KEY=your_secret_key_here### Build for Production# Build frontendnpm run build# Output will be in dist/ directory# Deploy dist/ to your hosting service### Troubleshooting1. **Port already in use**:   - Change port in `vite.config.ts` or kill process using port 80802. **Module not found errors**:   - Run `npm install` again   - Check that all dependencies are in `package.json`3. **Airflow DAG not showing**:   - Check DAG file syntax   - Verify Python path includes project root   - Check Airflow logs for errors4. **TypeScript errors**:   - Run `npm run lint` to see detailed errors   - Ensure all imports are correct## 📝 Development Notes- The frontend currently uses mock data (`src/lib/mockData.ts`) for development- To connect to real data, implement API endpoints and update TanStack Query hooks- Airflow DAGs run every 6 hours by default (configurable in `dags.py`)- Risk score weights can be adjusted in `models/risk_models.py`## 🤝 Contributing1. Fork the repository2. Create a feature branch (`git checkout -b feature/amazing-feature`)3. Commit your changes (`git commit -m 'Add amazing feature'`)4. Push to the branch (`git push origin feature/amazing-feature`)5. Open a Pull Request## 📄 License[Specify your license here]## 👥 Authors[Your name/team]---**Built with ❤️ using React, TypeScript, Python, and Apache Airflow**
Default Weights:
Volatility: 35%
Liquidity: 25%
Sentiment: 20%
Momentum: 20%
Score Range: 0-100 (lower = lower risk)
🧩 Project Components
Frontend Components
Pages
Index.tsx: Landing page displaying top 20 coins, search bar, and feature highlights
CoinDetail.tsx: Individual coin analysis page with detailed metrics, charts, and risk breakdown
NotFound.tsx: 404 error page
Reusable Components
CoinCard.tsx: Displays coin information in a card format with risk score, price, and metrics
SearchBar.tsx: Search functionality with autocomplete suggestions
StabilityChart.tsx: Interactive price chart with moving averages and volatility bands
MetricsPanel.tsx: Displays risk score, volatility, liquidity, and sentiment metrics
UI Components (src/components/ui/)
Built on Radix UI primitives
Fully accessible and customizable
Includes: buttons, cards, dialogs, forms, charts, and more
Backend Components
ETL Pipeline
extract_coingecko.py: CoinGecko API client with rate limiting and error handling
extracts_binance.py: Binance API client for orderbook data
transform_cleaning.py: Data validation and cleaning utilities
features.py: Feature engineering functions (rolling stats, technical indicators)
loads.py: Data serialization and storage utilities
Risk Modeling
risk_models.py: Composite risk score computation with configurable weights
Orchestration
airflow/dags.py: Airflow DAG definition for automated ETL pipeline execution
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