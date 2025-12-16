"""
Quick test script to check sample data
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from predictor.sample_data import create_sample_bbri_data
from datetime import datetime

print("Testing sample data generation...")
print("=" * 60)

df = create_sample_bbri_data(240)

print(f"✓ Data shape: {df.shape}")
print(f"✓ Columns: {list(df.columns)}")
print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
print(f"✓ Last date: {df['date'].iloc[-1]}")
print(f"✓ Today: {datetime.now().date()}")
print(f"✓ Days from last date to today: {(datetime.now().date() - df['date'].iloc[-1].date()).days}")

print("\nLast 5 rows:")
print(df[['date', 'close']].tail())

print("\n" + "=" * 60)
print("Sample data test completed!")
