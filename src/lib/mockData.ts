import { Coin, CoinDetail, PricePoint } from "@/types/crypto";

export const mockTopCoins: Coin[] = [
  {
    id: "bitcoin",
    symbol: "BTC",
    name: "Bitcoin",
    current_price: 67234.50,
    price_change_24h: 1234.50,
    price_change_percentage_24h: 1.87,
    market_cap: 1320000000000,
    total_volume: 28500000000,
    rank: 1,
    risk_score: 32,
    volatility_score: 28,
    liquidity_score: 95,
    sentiment_score: 72,
  },
  {
    id: "ethereum",
    symbol: "ETH",
    name: "Ethereum",
    current_price: 3456.78,
    price_change_24h: 89.23,
    price_change_percentage_24h: 2.65,
    market_cap: 415000000000,
    total_volume: 15200000000,
    rank: 2,
    risk_score: 35,
    volatility_score: 31,
    liquidity_score: 92,
    sentiment_score: 68,
  },
  {
    id: "binancecoin",
    symbol: "BNB",
    name: "BNB",
    current_price: 612.34,
    price_change_24h: -12.45,
    price_change_percentage_24h: -1.99,
    market_cap: 89000000000,
    total_volume: 1800000000,
    rank: 3,
    risk_score: 42,
    volatility_score: 38,
    liquidity_score: 85,
    sentiment_score: 61,
  },
  {
    id: "solana",
    symbol: "SOL",
    name: "Solana",
    current_price: 178.92,
    price_change_24h: 5.67,
    price_change_percentage_24h: 3.27,
    market_cap: 78000000000,
    total_volume: 3200000000,
    rank: 4,
    risk_score: 48,
    volatility_score: 52,
    liquidity_score: 78,
    sentiment_score: 75,
  },
  {
    id: "cardano",
    symbol: "ADA",
    name: "Cardano",
    current_price: 0.67,
    price_change_24h: 0.02,
    price_change_percentage_24h: 3.08,
    market_cap: 23500000000,
    total_volume: 890000000,
    rank: 5,
    risk_score: 39,
    volatility_score: 35,
    liquidity_score: 81,
    sentiment_score: 64,
  },
  {
    id: "ripple",
    symbol: "XRP",
    name: "XRP",
    current_price: 0.52,
    price_change_24h: 0.015,
    price_change_percentage_24h: 2.97,
    market_cap: 27000000000,
    total_volume: 1200000000,
    rank: 6,
    risk_score: 41,
    volatility_score: 39,
    liquidity_score: 83,
    sentiment_score: 66,
  },
  {
    id: "polkadot",
    symbol: "DOT",
    name: "Polkadot",
    current_price: 7.82,
    price_change_24h: -0.23,
    price_change_percentage_24h: -2.85,
    market_cap: 10500000000,
    total_volume: 420000000,
    rank: 7,
    risk_score: 44,
    volatility_score: 46,
    liquidity_score: 76,
    sentiment_score: 63,
  },
  {
    id: "dogecoin",
    symbol: "DOGE",
    name: "Dogecoin",
    current_price: 0.08,
    price_change_24h: 0.003,
    price_change_percentage_24h: 3.89,
    market_cap: 11200000000,
    total_volume: 650000000,
    rank: 8,
    risk_score: 53,
    volatility_score: 58,
    liquidity_score: 74,
    sentiment_score: 71,
  },
  {
    id: "avalanche",
    symbol: "AVAX",
    name: "Avalanche",
    current_price: 38.45,
    price_change_24h: 1.23,
    price_change_percentage_24h: 3.31,
    market_cap: 14800000000,
    total_volume: 580000000,
    rank: 9,
    risk_score: 46,
    volatility_score: 50,
    liquidity_score: 77,
    sentiment_score: 69,
  },
  {
    id: "chainlink",
    symbol: "LINK",
    name: "Chainlink",
    current_price: 14.67,
    price_change_24h: -0.34,
    price_change_percentage_24h: -2.26,
    market_cap: 8600000000,
    total_volume: 380000000,
    rank: 10,
    risk_score: 43,
    volatility_score: 44,
    liquidity_score: 79,
    sentiment_score: 67,
  },
  {
    id: "polygon",
    symbol: "MATIC",
    name: "Polygon",
    current_price: 0.89,
    price_change_24h: 0.042,
    price_change_percentage_24h: 4.95,
    market_cap: 8200000000,
    total_volume: 340000000,
    rank: 11,
    risk_score: 45,
    volatility_score: 48,
    liquidity_score: 75,
    sentiment_score: 70,
  },
  {
    id: "litecoin",
    symbol: "LTC",
    name: "Litecoin",
    current_price: 84.23,
    price_change_24h: 2.15,
    price_change_percentage_24h: 2.62,
    market_cap: 6300000000,
    total_volume: 420000000,
    rank: 12,
    risk_score: 38,
    volatility_score: 36,
    liquidity_score: 82,
    sentiment_score: 65,
  },
  {
    id: "uniswap",
    symbol: "UNI",
    name: "Uniswap",
    current_price: 6.78,
    price_change_24h: -0.18,
    price_change_percentage_24h: -2.59,
    market_cap: 5100000000,
    total_volume: 180000000,
    rank: 13,
    risk_score: 47,
    volatility_score: 51,
    liquidity_score: 73,
    sentiment_score: 68,
  },
  {
    id: "stellar",
    symbol: "XLM",
    name: "Stellar",
    current_price: 0.12,
    price_change_24h: 0.004,
    price_change_percentage_24h: 3.45,
    market_cap: 3400000000,
    total_volume: 145000000,
    rank: 14,
    risk_score: 42,
    volatility_score: 43,
    liquidity_score: 78,
    sentiment_score: 64,
  },
  {
    id: "cosmos",
    symbol: "ATOM",
    name: "Cosmos",
    current_price: 9.56,
    price_change_24h: 0.32,
    price_change_percentage_24h: 3.46,
    market_cap: 3700000000,
    total_volume: 215000000,
    rank: 15,
    risk_score: 45,
    volatility_score: 47,
    liquidity_score: 76,
    sentiment_score: 66,
  },
  {
    id: "monero",
    symbol: "XMR",
    name: "Monero",
    current_price: 162.34,
    price_change_24h: -3.21,
    price_change_percentage_24h: -1.94,
    market_cap: 2900000000,
    total_volume: 95000000,
    rank: 16,
    risk_score: 49,
    volatility_score: 53,
    liquidity_score: 71,
    sentiment_score: 62,
  },
  {
    id: "ethereum-classic",
    symbol: "ETC",
    name: "Ethereum Classic",
    current_price: 26.78,
    price_change_24h: 0.89,
    price_change_percentage_24h: 3.44,
    market_cap: 3800000000,
    total_volume: 185000000,
    rank: 17,
    risk_score: 51,
    volatility_score: 55,
    liquidity_score: 72,
    sentiment_score: 60,
  },
  {
    id: "algorand",
    symbol: "ALGO",
    name: "Algorand",
    current_price: 0.18,
    price_change_24h: 0.007,
    price_change_percentage_24h: 4.05,
    market_cap: 1400000000,
    total_volume: 82000000,
    rank: 18,
    risk_score: 44,
    volatility_score: 46,
    liquidity_score: 74,
    sentiment_score: 67,
  },
  {
    id: "vechain",
    symbol: "VET",
    name: "VeChain",
    current_price: 0.025,
    price_change_24h: 0.0008,
    price_change_percentage_24h: 3.31,
    market_cap: 1800000000,
    total_volume: 68000000,
    rank: 19,
    risk_score: 48,
    volatility_score: 52,
    liquidity_score: 70,
    sentiment_score: 65,
  },
  {
    id: "filecoin",
    symbol: "FIL",
    name: "Filecoin",
    current_price: 5.23,
    price_change_24h: -0.15,
    price_change_percentage_24h: -2.79,
    market_cap: 2500000000,
    total_volume: 125000000,
    rank: 20,
    risk_score: 50,
    volatility_score: 54,
    liquidity_score: 69,
    sentiment_score: 63,
  },
];

export const generateMockPriceData = (days: number): PricePoint[] => {
  const now = Date.now();
  const points: PricePoint[] = [];
  let price = 50000 + Math.random() * 20000;
  
  for (let i = days * 24; i >= 0; i--) {
    const volatility = Math.random() * 0.05;
    const change = (Math.random() - 0.5) * price * volatility;
    price = Math.max(price + change, 1000);
    
    const point: PricePoint = {
      timestamp: now - i * 3600000,
      price: price,
      volume: Math.random() * 1000000000,
      volatility: volatility,
    };
    
    points.push(point);
  }
  
  // Calculate moving averages
  points.forEach((point, idx) => {
    if (idx >= 7) {
      const ma7 = points.slice(idx - 7, idx).reduce((sum, p) => sum + p.price, 0) / 7;
      point.ma_7 = ma7;
    }
    if (idx >= 30) {
      const ma30 = points.slice(idx - 30, idx).reduce((sum, p) => sum + p.price, 0) / 30;
      point.ma_30 = ma30;
    }
  });
  
  return points;
};

export const getMockCoinDetail = (coinId: string): CoinDetail => {
  const coin = mockTopCoins.find(c => c.id === coinId);
  
  if (coin) {
    return {
      ...coin,
      market_cap_rank: coin.rank,
      ath: coin.current_price * 1.5,
      ath_change_percentage: -33.3,
      atl: coin.current_price * 0.1,
      atl_change_percentage: 900,
      circulating_supply: coin.market_cap / coin.current_price,
      max_supply: coin.market_cap / coin.current_price * 1.2,
      description: `${coin.name} is a decentralized cryptocurrency that operates on a blockchain network.`,
    };
  }
  
  // Generate dynamic mock data for any searched coin
  return generateDynamicCoinData(coinId);
};

export const generateDynamicCoinData = (coinId: string): CoinDetail => {
  // Create deterministic but varied data based on coin name
  const hash = coinId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const seed = hash % 100;
  
  const basePrice = 10 + (seed * 100);
  const marketCap = (basePrice * 1e6) * (10 + seed * 5);
  const volume = marketCap * 0.15;
  const priceChange = (seed % 20) - 10;
  
  const name = coinId.charAt(0).toUpperCase() + coinId.slice(1);
  const symbol = coinId.slice(0, 4).toUpperCase();
  
  return {
    id: coinId,
    symbol: symbol,
    name: name,
    current_price: basePrice,
    price_change_24h: (basePrice * priceChange) / 100,
    price_change_percentage_24h: priceChange,
    market_cap: marketCap,
    total_volume: volume,
    rank: 21 + (seed % 500),
    risk_score: 25 + (seed % 50),
    volatility_score: 20 + (seed % 60),
    liquidity_score: 40 + (seed % 55),
    sentiment_score: 30 + (seed % 65),
    market_cap_rank: 21 + (seed % 500),
    ath: basePrice * 2.5,
    ath_change_percentage: -45 - (seed % 30),
    atl: basePrice * 0.05,
    atl_change_percentage: 1500 + (seed % 500),
    circulating_supply: marketCap / basePrice,
    max_supply: (marketCap / basePrice) * 1.5,
    description: `${name} is an emerging cryptocurrency with innovative blockchain technology. Our risk analysis algorithms track real-time market data, sentiment, and on-chain metrics to provide comprehensive risk assessment.`,
  };
};

export const searchCoins = (query: string): Coin[] => {
  if (!query || query.length < 2) return [];
  
  const lowerQuery = query.toLowerCase();
  
  // First, search in top 20
  const topResults = mockTopCoins.filter(
    coin =>
      coin.name.toLowerCase().includes(lowerQuery) ||
      coin.symbol.toLowerCase().includes(lowerQuery)
  );
  
  // If we have results from top 20, return them
  if (topResults.length > 0) {
    return topResults.slice(0, 5);
  }
  
  // Otherwise, generate dynamic results for any search term
  // Simulate finding coins in our "database of 10,000+"
  const dynamicCoin = generateDynamicCoinData(lowerQuery);
  return [dynamicCoin];
};
