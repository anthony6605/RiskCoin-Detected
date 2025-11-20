# Crypto Risk Analyzer

A comprehensive cryptocurrency risk analysis platform that provides real-time risk scoring, volatility analysis, and investment insights for 10,000+ cryptocurrencies. The platform combines data engineering pipelines, machine learning models, and a modern web interface to deliver actionable risk metrics.

<img width="2048" height="1225" alt="f75e9c56-7dd7-4300-935e-69cfd5ab3e30" src="https://github.com/user-attachments/assets/f4376abb-c35d-4007-94c3-76ec1f323b97" />

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

## 📊 System Architecture Diagram
<img width="1024" height="1024" alt="System Architecture" src="https://github.com/user-attachments/assets/6d6a0bc0-f24b-45a1-ae2d-b7eb80f4253d" />


## 🧩 Component Breakdown Diagram

<img width="1024" height="1024" alt="Component Breakdown" src="https://github.com/user-attachments/assets/04401980-8df9-4cf5-9672-29697e657d7c" />

🚀 User Setup
```python
    pip install pandas
```


✅ Setup Instructions
🔧 Prerequisites
Node.js 18+ and npm

Python 3.9+

Apache Airflow (for ETL pipeline)

Git

📦 Install Python Dependencies
```bash
    pip install -r requirements.txt
```

🚀 Frontend Setup
Clone the repository
markdown
Copy code

```bash
    git clone <repository-url>
    cd RiskCoin-Detected
```
Install dependencies
markdown
Copy code
```bash
    npm install
```
Start development server
markdown
Copy code
```bash
    npm run dev
```
Access the application
Open:
http://localhost:8080

🛠 Backend / Data Pipeline Setup
Create Python virtual environment
markdown
Copy code
```bash
    python3 -m venv venv
    source venv/bin/activate      # macOS / Linux
    # Windows:
    # venv\Scripts\activate
```
Install Python dependencies
markdown
Copy code
```bash
    pip install pandas numpy requests apache-airflow
```
⚙️ Airflow Configuration
Initialize Airflow database
markdown
Copy code
```bash
    airflow db init
```
Create admin user
markdown
Copy code
```bash
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com
```
Start Airflow
markdown
Copy code
```bash
    airflow webserver --port 8080
```
markdown
Copy code
```bash
    airflow scheduler
```
🗂 Update DAG Paths (if needed)
Edit airflow/dags.py to match your project path

Ensure the source/ directory is included in the Python path

🧪 Run ETL Pipeline Manually (Optional)
markdown
Copy code
```bash
    python -m source.extract_coingecko
    python -m source.extracts_binance
```
🔐 Environment Variables
Create a .env file in the root:

markdown
Copy code
```env
    COINGECKO_API_KEY=your_api_key_here
    BINANCE_API_KEY=your_api_key_here
    BINANCE_SECRET_KEY=your_secret_key_here
```
🏗 Build for Production
markdown
Copy code
```bash
    npm run build
```
Output will be located in:

dist/ directory

Deploy dist/ to your hosting provider

❗ Troubleshooting
Port already in use
Change port in vite.config.ts

Or stop the process using port 8080

Module not found
Run npm install again

Ensure all deps exist in package.json

Airflow DAG not showing
Check DAG file syntax

Ensure project root is in Python path

Check Airflow logs

TypeScript errors
markdown
Copy code
```bash
    npm run lint
```

📝 Development Notes
The frontend currently uses mock data (src/lib/mockData.ts) for development
To connect to real data, implement API endpoints and update TanStack Query hooks
Airflow DAGs run every 6 hours by default (configurable in dags.py)
Risk score weights can be adjusted in models/risk_models.py
