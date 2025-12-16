"""
Utility to create sample/demo data when yfinance is not available
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import ta


def create_sample_bbri_data(days=240):
    """
    Create realistic sample BBRI stock data for demo purposes
    Data will end at yesterday (to allow predictions for today and future)
    
    Args:
        days: Number of days of historical data to generate
        
    Returns:
        DataFrame with BBRI-like stock data
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate dates BACKWARDS from yesterday (excluding weekends)
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    dates = []
    current_date = end_date
    
    # Go backwards until we have enough trading days
    while len(dates) < days:
        if current_date.weekday() < 5:  # Monday to Friday only
            dates.insert(0, current_date)  # Insert at beginning
        current_date -= timedelta(days=1)  # Go back one day
    
    # Generate realistic BBRI price data
    # BBRI typically trades around 4500-5500 IDR
    base_price = 5000
    volatility = 0.015  # 1.5% daily volatility
    trend = 0.0002  # Slight upward trend
    
    prices = [base_price]
    for i in range(1, len(dates)):
        # Random walk with drift
        change = np.random.normal(trend, volatility)
        new_price = prices[-1] * (1 + change)
        # Keep price in realistic range
        new_price = max(4200, min(5800, new_price))
        prices.append(new_price)
    
    # Create OHLCV data
    df = pd.DataFrame({
        'date': dates,
        'open': [p * (1 + np.random.uniform(-0.005, 0.005)) for p in prices],
        'high': [p * (1 + np.random.uniform(0.005, 0.02)) for p in prices],
        'low': [p * (1 + np.random.uniform(-0.02, -0.005)) for p in prices],
        'close': prices,
        'volume': [np.random.randint(50000000, 200000000) for _ in prices]
    })
    
    # Ensure high is highest and low is lowest
    df['high'] = df[['open', 'high', 'close']].max(axis=1)
    df['low'] = df[['open', 'low', 'close']].min(axis=1)
    
    # Add technical indicators
    df['ma_7'] = df['close'].rolling(window=7).mean()
    df['ma_30'] = df['close'].rolling(window=30).mean()
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
    
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    
    bollinger = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_upper'] = bollinger.bollinger_hband()
    df['bb_middle'] = bollinger.bollinger_mavg()
    df['bb_lower'] = bollinger.bollinger_lband()
    
    # Add TFT-specific columns
    df['time_idx'] = range(len(df))
    df['series'] = 'BBRI'
    df['target'] = df['close']
    
    # Remove NaN values
    df = df.dropna().reset_index(drop=True)
    df['time_idx'] = range(len(df))
    
    return df


def get_latest_sample_price():
    """Get the latest price from sample data"""
    df = create_sample_bbri_data(days=10)
    return df['close'].iloc[-1]
