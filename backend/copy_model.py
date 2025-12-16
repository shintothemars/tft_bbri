"""
Script to copy the trained model to the correct location
Run this after training your model
"""
import shutil
import os

# Source: where your model is currently
source_model = "best_tft_model.pth"

# Destination: project root
destination = os.path.join(os.path.dirname(__file__), "..", "best_tft_model.pth")

if os.path.exists(source_model):
    shutil.copy2(source_model, destination)
    print(f"✓ Model copied successfully to {destination}")
else:
    print(f"❌ Model file not found at {source_model}")
    print("Please ensure you have trained the model first using bussiness_intelegen.py")
