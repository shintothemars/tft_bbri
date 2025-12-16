# ⚡ Quick Reference Guide

## 🚀 Quick Start Commands

### First Time Setup

```powershell
# Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate

# Frontend Setup (new terminal)
cd frontend
npm install
```

### Daily Usage

```powershell
# Option 1: Use start script (Windows)
.\start.bat

# Option 2: Manual start
# Terminal 1 - Backend
cd backend
.\venv\Scripts\activate
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 📍 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main application |
| Backend API | http://localhost:8000/api/ | REST API |
| Health Check | http://localhost:8000/api/health/ | API status |
| Django Admin | http://localhost:8000/admin/ | Admin panel |

---

## 📂 Key Files

### Configuration
- `backend/bbri_backend/settings.py` - Django settings
- `frontend/vite.config.js` - Vite config
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies

### Core Logic
- `backend/predictor/model.py` - TFT model loader
- `backend/predictor/views.py` - API endpoints
- `frontend/src/App.jsx` - Main React app
- `frontend/src/components/PredictionForm.jsx` - Input form
- `frontend/src/components/PredictionResults.jsx` - Results display

### Documentation
- `README.md` - Main documentation
- `INSTALL.md` - Installation guide
- `API_DOCUMENTATION.md` - API reference
- `PANDUAN_PENGGUNA.md` - User guide (Indonesian)
- `DEPLOYMENT.md` - Production deployment
- `PROJECT_SUMMARY.md` - Project overview

---

## 🔧 Common Commands

### Backend

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Run server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Test backend
python test_backend.py

# Collect static files
python manage.py collectstatic
```

### Frontend

```powershell
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🧪 Testing

### Test Backend
```powershell
cd backend
.\venv\Scripts\activate
python test_backend.py
```

### Test API Manually
```powershell
# Health check
curl http://localhost:8000/api/health/

# Prediction
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d "{\"target_date\": \"2025-12-31\"}"
```

---

## 🐛 Quick Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
python manage.py runserver 8001
```

**Module not found:**
```powershell
pip install -r requirements.txt
```

**Model file not found:**
- Ensure `best_tft_model.pth` is in root directory
- Check path in `settings.py`

### Frontend Issues

**Port 3000 already in use:**
- Edit `vite.config.js`, change port to 3001

**Dependencies error:**
```powershell
rm -rf node_modules package-lock.json
npm install
```

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check proxy in `vite.config.js`

---

## 📊 API Quick Reference

### Health Check
```http
GET /api/health/
```

### Predict Stock Price
```http
POST /api/predict/
Content-Type: application/json

{
  "target_date": "2025-12-31"
}
```

**Response Fields:**
- `predictions.median` - Main prediction
- `predictions.lower_bound` - 10th percentile
- `predictions.upper_bound` - 90th percentile
- `analysis.trend_direction` - "NAIK" or "TURUN"
- `bokeh_plot` - Chart data for rendering

---

## 🎨 Customization Quick Tips

### Change Colors (Frontend)
Edit `frontend/src/index.css`:
```css
:root {
  --primary-color: #667eea;  /* Change this */
  --secondary-color: #764ba2; /* And this */
}
```

### Change Prediction Horizon (Backend)
Edit `backend/predictor/model.py`:
```python
self.max_prediction_length = 30  # Change to desired days
```

### Change Port (Backend)
```powershell
python manage.py runserver 0.0.0.0:8001
```

### Change Port (Frontend)
Edit `frontend/vite.config.js`:
```javascript
server: {
  port: 3001  // Change this
}
```

---

## 📦 Dependencies Overview

### Backend (Python)
- Django 4.2 - Web framework
- djangorestframework - API
- torch - PyTorch
- pytorch-forecasting - TFT model
- yfinance - Stock data
- bokeh - Visualization
- ta - Technical analysis

### Frontend (JavaScript)
- react 18 - UI library
- vite 5 - Build tool
- axios - HTTP client
- date-fns - Date utilities

---

## 🔐 Environment Variables (Production)

Create `.env` in `backend/`:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bbri_prediction
DB_USER=your_user
DB_PASSWORD=your_password
```

---

## 📈 Model Information

- **Type:** Temporal Fusion Transformer
- **Encoder Length:** 60 days
- **Prediction Length:** Max 30 days
- **Features:** 13 (price + technical indicators)
- **Quantiles:** 7 (0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98)

---

## 🎯 Project Structure (Simplified)

```
tft_bbri/
├── backend/
│   ├── bbri_backend/      # Settings
│   ├── predictor/         # Main app
│   └── manage.py
├── frontend/
│   └── src/
│       ├── components/    # React components
│       └── App.jsx
├── best_tft_model.pth     # Trained model
└── start.bat              # Quick start script
```

---

## 💡 Tips & Best Practices

### Development
- Always activate virtual environment before running backend
- Use `npm run dev` for frontend hot reload
- Check browser console for frontend errors
- Check terminal for backend errors

### Testing
- Test backend with `test_backend.py` before starting
- Test API with curl or Postman
- Test frontend in multiple browsers

### Deployment
- Never commit `.env` files
- Use environment variables for secrets
- Set DEBUG=False in production
- Use HTTPS in production

---

## 📞 Getting Help

1. **Check Documentation:**
   - README.md for overview
   - INSTALL.md for setup
   - API_DOCUMENTATION.md for API details
   - PANDUAN_PENGGUNA.md for user guide

2. **Run Tests:**
   - `python test_backend.py` for backend
   - Check browser console for frontend

3. **Common Issues:**
   - See troubleshooting section above
   - Check GitHub issues (if applicable)

---

## ⚡ Keyboard Shortcuts (Browser)

- `F5` - Refresh page
- `Ctrl + Shift + I` - Open DevTools
- `Ctrl + Shift + R` - Hard refresh (clear cache)
- `F12` - Toggle DevTools

---

## 🎓 Learning Resources

### Django
- https://docs.djangoproject.com/
- https://www.django-rest-framework.org/

### React
- https://react.dev/
- https://vitejs.dev/

### PyTorch Forecasting
- https://pytorch-forecasting.readthedocs.io/

### Bokeh
- https://docs.bokeh.org/

---

**Quick Reference Version 1.0**
*Last Updated: December 2025*
