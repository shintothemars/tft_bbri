"""
Model loader and predictor for TFT model
"""
import os
import torch
import pandas as pd
import numpy as np
import yfinance as yf
import ta
from datetime import datetime, timedelta
from pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer
from pytorch_forecasting.data import GroupNormalizer
from pytorch_forecasting.metrics import QuantileLoss
from django.conf import settings
from .sample_data import create_sample_bbri_data



class TFTPredictor:
    """
    Temporal Fusion Transformer predictor for BBRI stock
    """
    
    def __init__(self):
        self.model = None
        self.training_dataset = None
        self.max_encoder_length = 60
        self.max_prediction_length = 30
        self.ticker = "BBRI.JK"
        
    def load_model(self):
        """Load the trained TFT model"""
        if self.model is not None:
            return self.model
            
        try:
            # First, we need to create a dummy dataset to initialize the model architecture
            dummy_data = self._create_dummy_dataset()
            
            # Create model from dataset
            self.model = TemporalFusionTransformer.from_dataset(
                dummy_data,
                learning_rate=0.03,
                hidden_size=32,
                attention_head_size=2,
                dropout=0.1,
                hidden_continuous_size=16,
                output_size=7,  # 7 quantiles
                loss=QuantileLoss(),
                reduce_on_plateau_patience=4,
            )
            
            # Load the saved weights
            if os.path.exists(settings.MODEL_PATH):
                state_dict = torch.load(settings.MODEL_PATH, map_location=torch.device('cpu'))
                self.model.load_state_dict(state_dict)
                self.model.eval()
                print(f"✓ Model loaded successfully from {settings.MODEL_PATH}")
            else:
                print(f"⚠️ Model file not found at {settings.MODEL_PATH}. Using untrained model.")
                
            return self.model
            
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            raise
    
    def _create_dummy_dataset(self):
        """Create a minimal dummy dataset for model initialization"""
        # Create minimal data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        dummy_df = pd.DataFrame({
            'date': dates,
            'close': np.random.randn(100) * 100 + 5000,
            'open': np.random.randn(100) * 100 + 5000,
            'high': np.random.randn(100) * 100 + 5100,
            'low': np.random.randn(100) * 100 + 4900,
            'volume': np.random.randint(1000000, 10000000, 100),
        })
        
        # Add technical indicators (simplified)
        dummy_df['ma_7'] = dummy_df['close'].rolling(7).mean().fillna(dummy_df['close'])
        dummy_df['ma_30'] = dummy_df['close'].rolling(30).mean().fillna(dummy_df['close'])
        dummy_df['rsi'] = 50.0  # Simplified
        dummy_df['macd'] = 0.0
        dummy_df['macd_signal'] = 0.0
        dummy_df['bb_upper'] = dummy_df['close'] * 1.02
        dummy_df['bb_middle'] = dummy_df['close']
        dummy_df['bb_lower'] = dummy_df['close'] * 0.98
        
        # Add required TFT columns
        dummy_df['time_idx'] = range(len(dummy_df))
        dummy_df['series'] = 'BBRI'
        dummy_df['target'] = dummy_df['close']
        
        # Create TimeSeriesDataSet
        dataset = TimeSeriesDataSet(
            dummy_df,
            time_idx="time_idx",
            target="target",
            group_ids=["series"],
            min_encoder_length=self.max_encoder_length // 2,
            max_encoder_length=self.max_encoder_length,
            min_prediction_length=1,
            max_prediction_length=self.max_prediction_length,
            static_categoricals=["series"],
            time_varying_known_reals=["time_idx"],
            time_varying_unknown_reals=[
                "target", "open", "high", "low", "volume",
                "ma_7", "ma_30", "rsi", "macd", "macd_signal",
                "bb_upper", "bb_middle", "bb_lower"
            ],
            target_normalizer=GroupNormalizer(groups=["series"], transformation="softplus"),
            add_relative_time_idx=True,
            add_target_scales=True,
            add_encoder_length=True,
        )
        
        return dataset
    
    def fetch_and_prepare_data(self, lookback_days=180):
        """
        Fetch real-time data from yfinance and prepare it for prediction
        
        Args:
            lookback_days: Number of days to fetch for historical context
            
        Returns:
            Prepared DataFrame with technical indicators
        """
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Calculate date range
                end_date = datetime.now()
                start_date = end_date - timedelta(days=lookback_days + 60)  # Extra buffer for indicators
                
                print(f"📥 Fetching data for {self.ticker} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (Attempt {attempt + 1}/{max_retries})")
                
                # Download data with timeout
                df = yf.download(
                    self.ticker,
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d'),
                    progress=False,
                    timeout=30
                )
                
                # Check if data is empty
                if df is None or df.empty or len(df) == 0:
                    error_msg = f"No data returned from Yahoo Finance for ticker {self.ticker}"
                    if attempt < max_retries - 1:
                        print(f"⚠️ {error_msg}. Retrying in 2 seconds...")
                        time.sleep(2)
                        continue
                    else:
                        raise ValueError(f"{error_msg}. Please check: 1) Internet connection, 2) Ticker symbol is correct (BBRI.JK for Indonesian stocks), 3) Yahoo Finance service is available")
                
                print(f"✓ Data fetched successfully: {len(df)} rows")
                
                df.reset_index(inplace=True)
                
                # Flatten MultiIndex columns if they exist
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = [col[1] if col[0] == 'Price' else col[0] for col in df.columns.values]
                
                # Standardize column names
                new_columns = []
                for col in df.columns:
                    if col == 'Date':
                        new_columns.append('date')
                    else:
                        new_columns.append(col.lower().replace(' ', '_'))
                df.columns = new_columns
                
                # Keep only necessary columns
                cols_to_keep = ['date', 'open', 'high', 'low', 'close', 'volume']
                missing_cols = [col for col in cols_to_keep if col not in df.columns]
                if missing_cols:
                    raise ValueError(f"Missing required columns: {missing_cols}. Available columns: {list(df.columns)}")
                
                df = df[[col for col in cols_to_keep if col in df.columns]].copy()
                
                # Add technical indicators
                df = self._add_technical_indicators(df)
                
                # Add TFT-specific columns
                df['time_idx'] = range(len(df))
                df['series'] = 'BBRI'
                df['target'] = df['close']
                
                # Remove NaN values
                df = df.dropna().reset_index(drop=True)
                
                # Update time_idx after dropping NaN
                df['time_idx'] = range(len(df))
                
                if len(df) < self.max_encoder_length:
                    raise ValueError(f"Insufficient data after preprocessing. Got {len(df)} rows, need at least {self.max_encoder_length}")
                
                print(f"✓ Data prepared successfully: {len(df)} rows after preprocessing")
                return df
                
            except Exception as e:
                error_msg = f"Error fetching data (attempt {attempt + 1}/{max_retries}): {str(e)}"
                print(f"❌ {error_msg}")
                
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    # Use sample data as fallback
                    print(f"\n⚠️ Yahoo Finance unavailable. Using SAMPLE DATA for demonstration.")
                    print(f"📊 This is realistic BBRI stock data generated for demo purposes.")
                    print(f"💡 For real predictions, ensure internet connection and Yahoo Finance access.\n")
                    
                    try:
                        df = create_sample_bbri_data(days=lookback_days + 60)
                        print(f"✓ Sample data loaded successfully: {len(df)} rows")
                        return df
                    except Exception as sample_error:
                        raise ValueError(f"Failed to fetch real data AND failed to create sample data. Original error: {str(e)}, Sample data error: {str(sample_error)}")
    
    def _add_technical_indicators(self, df):
        """Add technical indicators to the dataframe"""
        # Moving Averages
        df['ma_7'] = df['close'].rolling(window=7).mean()
        df['ma_30'] = df['close'].rolling(window=30).mean()
        
        # RSI
        df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
        
        # MACD
        macd = ta.trend.MACD(close=df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        
        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_upper'] = bollinger.bollinger_hband()
        df['bb_middle'] = bollinger.bollinger_mavg()
        df['bb_lower'] = bollinger.bollinger_lband()
        
        return df
    
    def predict(self, target_date):
        """
        Make prediction for a target date
        
        Args:
            target_date: Target date for prediction (datetime object or string)
            
        Returns:
            Dictionary containing predictions and metadata
        """
        try:
            # Load model if not already loaded
            if self.model is None:
                self.load_model()
            
            # Parse target date
            if isinstance(target_date, str):
                target_date = datetime.strptime(target_date, '%Y-%m-%d')
            
            # Fetch and prepare data
            df = self.fetch_and_prepare_data(lookback_days=180)
            
            # Get the last date in the data
            last_date = pd.to_datetime(df['date'].iloc[-1])
            
            # Calculate prediction horizon
            prediction_horizon = (target_date - last_date).days
            
            if prediction_horizon <= 0:
                raise ValueError(f"Target date must be in the future. Last available date: {last_date.strftime('%Y-%m-%d')}")
            
            if prediction_horizon > self.max_prediction_length:
                raise ValueError(f"Prediction horizon ({prediction_horizon} days) exceeds maximum ({self.max_prediction_length} days)")
            
            # Create dataset for prediction
            dataset = TimeSeriesDataSet(
                df,
                time_idx="time_idx",
                target="target",
                group_ids=["series"],
                min_encoder_length=self.max_encoder_length // 2,
                max_encoder_length=self.max_encoder_length,
                min_prediction_length=1,
                max_prediction_length=self.max_prediction_length,
                static_categoricals=["series"],
                time_varying_known_reals=["time_idx"],
                time_varying_unknown_reals=[
                    "target", "open", "high", "low", "volume",
                    "ma_7", "ma_30", "rsi", "macd", "macd_signal",
                    "bb_upper", "bb_middle", "bb_lower"
                ],
                target_normalizer=GroupNormalizer(groups=["series"], transformation="softplus"),
                add_relative_time_idx=True,
                add_target_scales=True,
                add_encoder_length=True,
            )
            
            # Create dataloader
            dataloader = dataset.to_dataloader(train=False, batch_size=1, num_workers=0)
            
            # Make prediction
            with torch.no_grad():
                raw_predictions = self.model.predict(dataloader, mode="prediction", return_x=False)
            
            # Extract predictions - handle different shapes
            predictions = raw_predictions.numpy()
            print(f"📊 Prediction shape: {predictions.shape}")
            
            # Handle different prediction shapes
            if len(predictions.shape) == 3:
                # Shape: [batch, prediction_length, quantiles]
                median_predictions = predictions[0, :prediction_horizon, 3]
                lower_bound = predictions[0, :prediction_horizon, 1]
                upper_bound = predictions[0, :prediction_horizon, 5]
            elif len(predictions.shape) == 2:
                # Shape: [prediction_length, quantiles]
                median_predictions = predictions[:prediction_horizon, 3]
                lower_bound = predictions[:prediction_horizon, 1]
                upper_bound = predictions[:prediction_horizon, 5]
            else:
                # Fallback: assume it's just median predictions
                print(f"⚠️ Unexpected prediction shape: {predictions.shape}")
                median_predictions = predictions.flatten()[:prediction_horizon]
                # Create simple confidence intervals (±10%)
                lower_bound = median_predictions * 0.9
                upper_bound = median_predictions * 1.1
            
            # Create prediction dates
            prediction_dates = [last_date + timedelta(days=i+1) for i in range(prediction_horizon)]
            
            # Prepare historical data (last 90 days)
            historical_days = 90
            historical_df = df.tail(historical_days).copy()
            
            # Calculate trend
            last_price = df['close'].iloc[-1]
            predicted_price = median_predictions[-1]
            trend_pct = ((predicted_price - last_price) / last_price) * 100
            
            return {
                'success': True,
                'target_date': target_date.strftime('%Y-%m-%d'),
                'last_data_date': last_date.strftime('%Y-%m-%d'),
                'prediction_horizon': prediction_horizon,
                'predictions': {
                    'dates': [d.strftime('%Y-%m-%d') for d in prediction_dates],
                    'median': median_predictions.tolist(),
                    'lower_bound': lower_bound.tolist(),
                    'upper_bound': upper_bound.tolist(),
                },
                'historical': {
                    'dates': historical_df['date'].dt.strftime('%Y-%m-%d').tolist(),
                    'close': historical_df['close'].tolist(),
                },
                'analysis': {
                    'last_price': float(last_price),
                    'predicted_price': float(predicted_price),
                    'trend_percentage': float(trend_pct),
                    'trend_direction': 'NAIK' if trend_pct > 0 else 'TURUN',
                    'confidence_range': {
                        'lower': float(lower_bound[-1]),
                        'upper': float(upper_bound[-1]),
                    }
                }
            }
            
        except Exception as e:
            print(f"❌ Error in prediction: {str(e)}")
            raise


# Global predictor instance
_predictor = None

def get_predictor():
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = TFTPredictor()
    return _predictor
