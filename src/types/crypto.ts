export interface Coin {
    id: string;
    symbol: string;
    name: string;
    current_price: number;
    price_change_24h: number;
    price_change_percentage_24h: number;
    market_cap: number;
    total_volume: number;
    rank: number;
    risk_score: number;
    volatility_score: number;
    liquidity_score: number;
    sentiment_score: number;
    image?: string;
  }
  
  export interface CoinDetail extends Coin {
    market_cap_rank: number;
    ath: number;
    ath_change_percentage: number;
    atl: number;
    atl_change_percentage: number;
    circulating_supply: number;
    max_supply: number;
    description?: string;
  }
  
  export interface PricePoint {
    timestamp: number;
    price: number;
    volume: number;
    volatility?: number;
    ma_7?: number;
    ma_30?: number;
  }
  
  export type TimeRange = "1D" | "7D" | "30D" | "90D" | "1Y";
  