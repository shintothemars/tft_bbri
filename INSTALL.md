# Quick Installation Guide

## Windows Installation

### 1. Setup Backend

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 2. Setup Frontend

Open a new terminal:

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Quick Start (Both Servers)

Double-click `start.bat` in the root directory, or run:

```powershell
.\start.bat
```

## Linux/Mac Installation

### 1. Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```

## Verification

1. Backend API: http://localhost:8000/api/health/
2. Frontend App: http://localhost:3000

## Common Issues

### PyTorch Installation
If PyTorch installation fails, try:
```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Node.js Version
Ensure Node.js version >= 16:
```powershell
node --version
```

### Port Already in Use
- Backend: Change port in `manage.py runserver 8001`
- Frontend: Change port in `vite.config.js`
