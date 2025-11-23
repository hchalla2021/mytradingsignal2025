@echo off
REM Quick Git Commit and Deploy to Render

echo ========================================
echo   Git Commit for Render Deployment
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
)

REM Add all files
echo Adding files to Git...
git add .

REM Commit with timestamp
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
git commit -m "Deploy to Render - %timestamp%"

echo.
echo ========================================
echo   Ready to Push!
echo ========================================
echo.
echo Next steps:
echo 1. Create GitHub repo: https://github.com/new
echo 2. Run: git remote add origin YOUR-REPO-URL
echo 3. Run: git push -u origin main
echo 4. Connect to Render.com dashboard
echo.
echo OR if remote already set:
echo   git push
echo.
pause
