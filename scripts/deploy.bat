@echo off
REM Quick Deploy Script for Market Signals (Windows)

echo ==================================
echo   Market Signals - Quick Deploy
echo ==================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - Market Signals Zerodha"
)

REM Menu
echo Choose deployment platform:
echo 1) Vercel (Recommended - Fast & Free)
echo 2) Railway (Backend-friendly)
echo 3) Render.com (Free tier)
echo 4) Docker (Local/Cloud)
echo 5) Exit
echo.
set /p choice="Enter choice [1-5]: "

if "%choice%"=="1" goto vercel
if "%choice%"=="2" goto railway
if "%choice%"=="3" goto render
if "%choice%"=="4" goto docker
if "%choice%"=="5" goto exit
goto invalid

:vercel
echo.
echo Deploying to Vercel...
echo.
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Vercel CLI...
    call npm i -g vercel
)
echo Running: vercel --prod
call vercel --prod
echo.
echo Deployment complete!
echo Don't forget to:
echo    1. Add environment variables in Vercel dashboard
echo    2. Update CORS in backend/main.py
goto end

:railway
echo.
echo Deploying to Railway...
echo.
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Railway CLI...
    call npm i -g @railway/cli
)
call railway login
call railway init
call railway up
echo.
echo Deployment complete!
echo Add environment variables in Railway dashboard
goto end

:render
echo.
echo Deploying to Render.com...
echo.
echo Please follow these steps:
echo 1. Go to https://render.com/dashboard
echo 2. Connect your Git repository
echo 3. Create two services:
echo    - Web Service (Backend): uvicorn main:app
echo    - Static Site (Frontend): npm run build
echo 4. Add environment variables
echo.
echo See DEPLOYMENT.md for detailed instructions
goto end

:docker
echo.
echo Building Docker containers...
echo.
docker-compose up --build
echo.
echo Docker containers running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
goto end

:exit
echo Exiting...
exit /b 0

:invalid
echo Invalid choice. Exiting...
exit /b 1

:end
echo.
echo ==================================
echo   Read DEPLOYMENT.md for details
echo ==================================
pause
