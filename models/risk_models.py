"""
Risk scoring model for cryptocurrencies.
Combines volatility, liquidity, sentiment, and on-chain metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def compute_risk_score(
    features_df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Compute composite risk score from features.
    
    Args:
        features_df: DataFrame with computed features
        weights: Component weights (default: equal weighting)
    
    Returns:
        DataFrame with risk_score column added
    """
    df = features_df.copy()
    
    # Default weights
    if weights is None:
        weights = {
            'volatility': 0.35,
            'liquidity': 0.25,
            'sentiment': 0.20,
            'momentum': 0.20
        }
    
    # Normalize components to 0-100 scale
    components = {}
    
    # Volatility score (higher vol = higher risk)
    if 'volatility_score' in df.columns:
        components['volatility'] = df['volatility_score']
    else:
        components['volatility'] = 50
    
    # Liquidity score (lower liquidity = higher risk)
    if 'liquidity_score' in df.columns:
        components['liquidity'] = 100 - df['liquidity_score']  # Invert
    else:
        components['liquidity'] = 50
    
    # Sentiment score (negative sentiment = higher risk)
    if 'sentiment_score' in df.columns:
        components['sentiment'] = 100 - df['sentiment_score']  # Invert
    else:
        components['sentiment'] = 50
    
    # Momentum score (extreme RSI = higher risk)
    if 'rsi' in df.columns:
        # Risk high when RSI < 30 (oversold) or > 70 (overbought)
        rsi_risk = np.where(df['rsi'] < 30, 30 - df['rsi'], 
                           np.where(df['rsi'] > 70, df['rsi'] - 70, 0))
        components['momentum'] = np.clip(rsi_risk * 2, 0, 100)
    else:
        components['momentum'] = 50
    
    # Weighted sum
    risk_score = sum(components[k] * weights[k] for k in weights.keys())
    df['risk_score'] = np.clip(risk_score, 0, 100).round(0).astype(int)
    
    return df


# Example usage
if __name__ == "__main__":
    sample_df = pd.DataFrame({
        'coin_id': ['bitcoin', 'ethereum', 'altcoin'],
        'volatility_score': [25, 35, 65],
        'liquidity_score': [95, 88, 45],
        'sentiment_score': [70, 65, 40],
        'rsi': [55, 45, 75]
    })
    
    result = compute_risk_score(sample_df)
    print(result[['coin_id', 'risk_score']])
