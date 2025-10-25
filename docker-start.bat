@echo off
REM Quick start script for Docker deployment (Windows)

echo 🐳 Zerion MCP Server - Docker Quick Start
echo ==========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker is not running
    echo Please start Docker Desktop
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo 📝 Creating .env file from example...
    copy .env.example .env >nul
    echo ⚠️  Please edit .env and set your ZERION_API_KEY
    echo    Then run this script again.
    pause
    exit /b 0
)

REM Check if API key is set (basic check)
findstr /C:"zk_dev_your_api_key_here" .env >nul
if not errorlevel 1 (
    echo ⚠️  Warning: ZERION_API_KEY in .env appears to be the example value
    echo    Please edit .env and set your actual API key
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

REM Create logs directory
if not exist logs mkdir logs

echo.
echo 🔨 Building Docker image...
docker-compose build

if errorlevel 1 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Zerion MCP Server...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Failed to start
    pause
    exit /b 1
)

echo.
echo ✅ Server is starting!
echo.
echo 📊 View logs:
echo    docker-compose logs -f
echo.
echo 🔍 Check status:
echo    docker-compose ps
echo.
echo 🛑 Stop server:
echo    docker-compose down
echo.
echo 📖 Full documentation: See DOCKER.md
echo.
pause
