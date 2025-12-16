"""
Test API endpoint directly
"""
import requests
import json

url = "http://localhost:8000/api/predict/"
data = {"target_date": "2025-12-23"}

print("Testing API endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")
print("=" * 60)

try:
    response = requests.post(url, json=data, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
