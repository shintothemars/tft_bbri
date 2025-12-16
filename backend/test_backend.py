"""
Test script to verify TFT model loading and prediction
Run this to test the backend without starting the full server
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bbri_backend.settings')
django.setup()

from predictor.model import get_predictor
from datetime import datetime, timedelta

def test_model_loading():
    """Test if model can be loaded"""
    print("=" * 80)
    print("Testing TFT Model Loading")
    print("=" * 80)
    
    try:
        predictor = get_predictor()
        predictor.load_model()
        print("✓ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def test_data_fetching():
    """Test if data can be fetched from yfinance"""
    print("\n" + "=" * 80)
    print("Testing Data Fetching")
    print("=" * 80)
    
    try:
        predictor = get_predictor()
        df = predictor.fetch_and_prepare_data(lookback_days=90)
        print(f"✓ Data fetched successfully!")
        print(f"  - Total rows: {len(df)}")
        print(f"  - Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"  - Columns: {', '.join(df.columns.tolist())}")
        return True
    except Exception as e:
        print(f"❌ Error fetching data: {str(e)}")
        return False

def test_prediction():
    """Test if prediction works"""
    print("\n" + "=" * 80)
    print("Testing Prediction")
    print("=" * 80)
    
    try:
        predictor = get_predictor()
        
        # Predict 7 days from now
        target_date = datetime.now() + timedelta(days=7)
        print(f"Target date: {target_date.strftime('%Y-%m-%d')}")
        
        result = predictor.predict(target_date)
        
        print("✓ Prediction successful!")
        print(f"\n  Analysis:")
        print(f"  - Last price: Rp {result['analysis']['last_price']:,.0f}")
        print(f"  - Predicted price: Rp {result['analysis']['predicted_price']:,.0f}")
        print(f"  - Trend: {result['analysis']['trend_direction']} ({result['analysis']['trend_percentage']:.2f}%)")
        print(f"  - Confidence range: Rp {result['analysis']['confidence_range']['lower']:,.0f} - Rp {result['analysis']['confidence_range']['upper']:,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n🧪 BBRI Stock Prediction - Backend Test Suite\n")
    
    results = []
    
    # Run tests
    results.append(("Model Loading", test_model_loading()))
    results.append(("Data Fetching", test_data_fetching()))
    results.append(("Prediction", test_prediction()))
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Backend is ready to use.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
