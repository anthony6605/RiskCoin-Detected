-- stablecoin_prices: raw time series of prices
CREATE TABLE stablecoin_prices (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  coin VARCHAR(32) NOT NULL,
  price_usd DOUBLE PRECISION NOT NULL,
  source VARCHAR(64),
  raw_json JSONB
);

-- stablecoin_metrics: processed metrics (deviation, volatility, spread)
CREATE TABLE stablecoin_metrics (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  coin VARCHAR(32) NOT NULL,
  price_usd DOUBLE PRECISION,
  deviation_pct DOUBLE PRECISION,
  volatility_7d DOUBLE PRECISION,
  avg_spread DOUBLE PRECISION,
  notes TEXT
);

-- risk_scores: final risk scoring
CREATE TABLE risk_scores (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  coin VARCHAR(32) NOT NULL,
  risk_score DOUBLE PRECISION,   
  risk_label VARCHAR(16),        
  features JSONB
);

-- alerts
CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT now(),
  coin VARCHAR(32),
  alert_type VARCHAR(64),
  message TEXT,
  metadata JSONB
);
