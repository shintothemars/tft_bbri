# Deployment Guide

## Production Deployment

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (recommended for production)
- Nginx (for reverse proxy)
- Gunicorn (for Django)

---

## Backend Deployment

### 1. Environment Setup

Create `.env` file in `backend/` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bbri_prediction
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Update Django Settings

Update `backend/bbri_backend/settings.py`:

```python
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
```

### 3. Install Production Dependencies

Add to `requirements.txt`:
```
gunicorn==21.2.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
```

Install:
```bash
pip install -r requirements.txt
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run with Gunicorn

```bash
gunicorn bbri_backend.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 6. Systemd Service (Linux)

Create `/etc/systemd/system/bbri-backend.service`:

```ini
[Unit]
Description=BBRI Prediction Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/tft_bbri/backend
Environment="PATH=/path/to/tft_bbri/backend/venv/bin"
ExecStart=/path/to/tft_bbri/backend/venv/bin/gunicorn \
          --workers 4 \
          --bind 0.0.0.0:8000 \
          bbri_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable bbri-backend
sudo systemctl start bbri-backend
```

---

## Frontend Deployment

### 1. Build Production Bundle

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized static files.

### 2. Serve with Nginx

Nginx configuration (`/etc/nginx/sites-available/bbri-prediction`):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /path/to/tft_bbri/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/tft_bbri/backend/staticfiles/;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/bbri-prediction /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Docker Deployment (Alternative)

### 1. Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "bbri_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build app
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./best_tft_model.pth:/app/best_tft_model.pth
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=bbri_prediction
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

---

## Cloud Deployment Options

### 1. Heroku

**Backend:**
```bash
cd backend
heroku create bbri-prediction-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

**Frontend:**
```bash
cd frontend
npm run build
# Deploy dist/ to Netlify or Vercel
```

### 2. AWS EC2

1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies (Python, Node.js, Nginx)
3. Follow Linux deployment steps above
4. Configure security groups (ports 80, 443)

### 3. Google Cloud Platform

Use Google Cloud Run for containerized deployment:
```bash
gcloud run deploy bbri-backend --source ./backend
gcloud run deploy bbri-frontend --source ./frontend
```

### 4. Azure

Use Azure App Service:
```bash
az webapp up --name bbri-prediction --runtime "PYTHON:3.10"
```

---

## Performance Optimization

### 1. Backend Caching

Add Redis caching in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Model Loading

Load model once at startup (singleton pattern already implemented).

### 3. Database Optimization

Use PostgreSQL with connection pooling:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,
    }
}
```

### 4. Frontend Optimization

- Enable gzip compression in Nginx
- Use CDN for static assets
- Implement lazy loading for charts

---

## Monitoring & Logging

### 1. Backend Logging

Update `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/bbri-backend.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Application Monitoring

Use tools like:
- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **Prometheus + Grafana** for metrics

---

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS (SSL certificate)
- [ ] Enable CSRF protection
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Use strong database passwords

---

## Backup Strategy

### Database Backup
```bash
# PostgreSQL
pg_dump bbri_prediction > backup_$(date +%Y%m%d).sql
```

### Model Backup
```bash
# Backup model file
cp best_tft_model.pth backups/best_tft_model_$(date +%Y%m%d).pth
```

---

## Troubleshooting Production Issues

### High Memory Usage
- Reduce number of Gunicorn workers
- Implement model caching
- Use smaller batch sizes

### Slow Predictions
- Enable Redis caching
- Optimize yfinance data fetching
- Use CDN for static assets

### Database Connection Errors
- Check connection pooling settings
- Verify database credentials
- Increase max connections

---

## Maintenance

### Regular Tasks
1. Update dependencies monthly
2. Monitor disk space
3. Review logs weekly
4. Backup database daily
5. Update SSL certificates (auto with Let's Encrypt)

### Model Updates
When retraining the model:
1. Train new model
2. Test with `test_backend.py`
3. Backup old model
4. Replace `best_tft_model.pth`
5. Restart backend service

---

For questions or issues, please refer to the main README.md or open an issue.
