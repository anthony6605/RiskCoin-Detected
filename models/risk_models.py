import pandas as pd 
import numpy as np 
from typing import Dict, Optional

#compute risk score from features
def compute_risk_score(
    features_df: pd.DataFrame,
    weights: Optional[Dict[str,float]] = None  
) -> pd.DataFrame:
    df = features_df.copy()

    if weights is None:
        weights = {
            'volatility': 0.35,
            'liquidity': 0.25,
            'sentiment': 0.20,
            'momentum': 0.20
        }
    components = {}

    #votality score(high vol = high risk)
    if 'volatility_score' in df.columns:
        components['volatility'] = df['volatility_score']
    else:
        components['volatility'] = 50   
    #liquidity score (low liquidity = high risk)
    if 'liquidity_score' in df.columns:
        components['liquidity'] = 100 - df['liquidity_score']  
    else:
        components['liquidity'] = 50 
    #sentiment score(negative sentiment = higher risk)
    if 'sentiment_score' in df.columns:
        components['sentiment'] = 100 - df['sentiment_score']  
    else:
        components['sentiment'] = 50
    #momentum_score(extreme RSI = higher risk)
    if 'rsi' in df.columns:
        # Risk high when RSI < 30 (oversold) or > 70 (overbought)
        rsi_risk = np.where(df['rsi'] < 30, 30 - df['rsi'], 
                           np.where(df['rsi'] > 70, df['rsi'] - 70, 0))
        components['momentum'] = np.clip(rsi_risk * 2, 0, 100)
    else:
        components['momentum'] = 50

    #weighted sum
    risk_score = sum(components[k] * weights[k] for k in weights.keys())
    df['risk_score'] = np.clip(risk_score, 0, 100).round(0).astype(int)
    
    return df

