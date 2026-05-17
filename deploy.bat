@echo off
REM deploy.bat - Quick deployment script for Railway (Windows)
REM Run: deploy.bat

echo ======================================================================
echo Aviation Intelligence Platform - Railway Deployment
echo ======================================================================
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo    Please create .env with your API keys before deploying.
    echo    Copy from .env.example and fill in your keys.
    pause
    exit /b 1
)

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo Git initialized
) else (
    echo Git repository already exists
)

REM Add and commit changes
echo.
echo Committing changes...
git add .
git commit -m "Aviation Intelligence Platform - Ready for deployment" -m "- Fixed f-string syntax error in cesium_map.py" -m "- Integrated accuracy improvements (holidays, fog alerts)" -m "- Enhanced ML model with new features" -m "- Added comprehensive documentation"
echo Changes committed
echo.

REM Check if remote exists
git remote | findstr /c:"origin" >nul 2>&1
if errorlevel 1 (
    echo No remote repository found.
    echo.
    set /p REPO_URL="Enter your GitHub repository URL: "

    if "%REPO_URL%"=="" (
        echo No repository URL provided. Exiting.
        pause
        exit /b 1
    )

    git remote add origin %REPO_URL%
    echo Remote added
)

REM Push to GitHub
echo.
echo Pushing to GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo Push failed. Trying to set branch to master...
    git branch -M main
    git push -u origin main -f
)

echo.
echo ======================================================================
echo Git deployment complete!
echo ======================================================================
echo.
echo Next steps:
echo.
echo 1. Go to https://railway.app/new
echo 2. Click 'Deploy from GitHub repo'
echo 3. Select your repository
echo 4. Add environment variables in Railway dashboard:
echo.
echo    Required:
echo    - AIRLABS_API_KEY
echo    - MAPBOX_TOKEN
echo.
echo    Recommended:
echo    - CHECKWX_API_KEY
echo.
echo 5. Click 'Deploy' and wait 2-3 minutes
echo 6. Railway will generate your live URL!
echo.
echo ======================================================================
echo Your Aviation Intelligence Platform will be live soon!
echo ======================================================================
echo.
pause
