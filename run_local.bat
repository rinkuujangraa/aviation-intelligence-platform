@echo off
REM Quick script to run the app locally

echo ========================================
echo Aviation Intelligence Platform - Local Run
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your API keys
    pause
    exit /b 1
)

echo Starting Streamlit app...
echo.
echo Your app will open at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

streamlit run app.py

pause
