"""
Simple test to check if model prediction works
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbri_backend.settings')
django.setup()

from predictor.model import get_predictor
from datetime import datetime, timedelta

print("Testing TFT Predictor...")
print("=" * 60)

try:
    # Get predictor
    predictor = get_predictor()
    print("✓ Predictor instance created")
    
    # Load model
    predictor.load_model()
    print("✓ Model loaded")
    
    # Test prediction
    target_date = datetime.now() + timedelta(days=7)
    print(f"\nTesting prediction for: {target_date.strftime('%Y-%m-%d')}")
    print("-" * 60)
    
    result = predictor.predict(target_date)
    
    print("\n✓ Prediction successful!")
    print(f"Last data date: {result['last_data_date']}")
    print(f"Prediction horizon: {result['prediction_horizon']} days")
    print(f"Last price: Rp {result['analysis']['last_price']:,.0f}")
    print(f"Predicted price: Rp {result['analysis']['predicted_price']:,.0f}")
    print(f"Trend: {result['analysis']['trend_direction']} ({result['analysis']['trend_percentage']:.2f}%)")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
