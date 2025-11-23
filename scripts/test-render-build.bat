@echo off
REM Render.com Local Test Script

echo ========================================
echo   Testing Render.com Build Locally
echo ========================================
echo.

echo [1/3] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend dependencies failed
    exit /b 1
)

echo.
echo [2/3] Installing frontend dependencies...
cd ..\frontend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend dependencies failed
    exit /b 1
)

echo.
echo [3/3] Building frontend...
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend build failed
    exit /b 1
)

echo.
echo ========================================
echo   Build Test Successful!
echo ========================================
echo.
echo You can now deploy to Render.com
echo See docs\RENDER_DEPLOY.md for instructions
echo.
pause
