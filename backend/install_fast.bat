@echo off
echo ========================================
echo   Installing Backend Dependencies
echo   (Optimized for faster installation)
echo ========================================
echo.

echo [1/3] Installing PyTorch (CPU version - faster)...
.\venv\Scripts\pip install torch --index-url https://download.pytorch.org/whl/cpu

echo.
echo [2/3] Installing other dependencies...
.\venv\Scripts\pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1

echo.
echo [3/3] Installing ML dependencies...
.\venv\Scripts\pip install pytorch-forecasting lightning pandas numpy yfinance ta bokeh scikit-learn python-dateutil

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
pause
