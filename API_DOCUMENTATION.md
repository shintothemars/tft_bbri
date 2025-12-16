# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health/`

**Response:**
```json
{
  "status": "healthy",
  "service": "BBRI Stock Prediction API",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### 2. Stock Price Prediction

Predict BBRI stock price for a target date.

**Endpoint:** `POST /predict/`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "target_date": "2025-12-31"
}
```

**Parameters:**
- `target_date` (string, required): Target date in YYYY-MM-DD format
  - Must be a future date
  - Maximum 30 days from the last available data

**Success Response (200 OK):**
```json
{
  "success": true,
  "target_date": "2025-12-31",
  "last_data_date": "2025-12-16",
  "prediction_horizon": 15,
  "predictions": {
    "dates": [
      "2025-12-17",
      "2025-12-18",
      "2025-12-19",
      ...
    ],
    "median": [5200.5, 5215.3, 5230.1, ...],
    "lower_bound": [5100.2, 5115.8, 5130.5, ...],
    "upper_bound": [5300.8, 5315.2, 5330.7, ...]
  },
  "historical": {
    "dates": ["2025-09-17", "2025-09-18", ...],
    "close": [5050.0, 5075.5, ...]
  },
  "analysis": {
    "last_price": 5150.0,
    "predicted_price": 5280.5,
    "trend_percentage": 2.53,
    "trend_direction": "NAIK",
    "confidence_range": {
      "lower": 5180.2,
      "upper": 5380.8
    }
  },
  "bokeh_plot": {
    "target_id": "bbri_prediction_plot",
    "root_id": "...",
    "doc": {...}
  }
}
```

**Error Responses:**

**400 Bad Request** - Invalid input
```json
{
  "error": "Parameter target_date diperlukan (format: YYYY-MM-DD)"
}
```

```json
{
  "error": "Format tanggal tidak valid. Gunakan format: YYYY-MM-DD"
}
```

```json
{
  "error": "Tanggal target harus di masa depan"
}
```

```json
{
  "error": "Prediction horizon (45 days) exceeds maximum (30 days)"
}
```

**500 Internal Server Error** - Server error
```json
{
  "error": "Terjadi kesalahan: [error message]"
}
```

---

## Response Fields Explanation

### predictions
- `dates`: Array of prediction dates
- `median`: Median predicted prices (50th percentile)
- `lower_bound`: Lower confidence bound (10th percentile)
- `upper_bound`: Upper confidence bound (90th percentile)

### historical
- `dates`: Array of historical dates (last 90 days)
- `close`: Closing prices for historical dates

### analysis
- `last_price`: Most recent actual closing price
- `predicted_price`: Predicted price for target date
- `trend_percentage`: Percentage change from last price
- `trend_direction`: "NAIK" (up) or "TURUN" (down)
- `confidence_range`: Range where actual price is likely to fall

### bokeh_plot
JSON representation of Bokeh plot for embedding in frontend.
Use `window.Bokeh.embed.embed_item()` to render.

---

## Example Usage

### cURL
```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"target_date": "2025-12-31"}'
```

### JavaScript (Axios)
```javascript
import axios from 'axios';

const response = await axios.post('/api/predict/', {
  target_date: '2025-12-31'
});

console.log(response.data);
```

### Python (requests)
```python
import requests

response = requests.post(
    'http://localhost:8000/api/predict/',
    json={'target_date': '2025-12-31'}
)

data = response.json()
print(data['analysis'])
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding rate limiting to prevent abuse.

---

## CORS

CORS is enabled for all origins in development mode. For production, update `CORS_ALLOW_ALL_ORIGINS` in `settings.py`.

---

## Notes

1. **Data Source**: Real-time data is fetched from Yahoo Finance using `yfinance` library
2. **Model**: Uses Temporal Fusion Transformer (TFT) with 60-day encoder length
3. **Technical Indicators**: Automatically calculates MA7, MA30, RSI, MACD, and Bollinger Bands
4. **Prediction Horizon**: Maximum 30 days from last available data
5. **Quantiles**: Model outputs 7 quantiles (0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98)

---

## Error Handling

The API uses standard HTTP status codes:
- `200 OK` - Request successful
- `400 Bad Request` - Invalid input parameters
- `500 Internal Server Error` - Server-side error

All errors return a JSON object with an `error` field containing the error message.
