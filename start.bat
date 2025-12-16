@echo off
echo ========================================
echo   BBRI Stock Prediction - Quick Start
echo ========================================
echo.

echo [1/4] Starting Backend (Django)...
cd backend
start cmd /k ".\venv\Scripts\activate && python manage.py runserver"
cd ..

timeout /t 3 /nobreak > nul

echo [2/4] Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo [3/4] Starting Frontend (React)...
cd frontend
start cmd /k "npm run dev"
cd ..

echo.
echo [4/4] Done!
echo.
echo ========================================
echo   Application is starting...
echo ========================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit this window...
pause > nul
