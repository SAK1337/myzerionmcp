#!/bin/bash
# Quick start script for Docker deployment

set -e

echo "🐳 Zerion MCP Server - Docker Quick Start"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and set your ZERION_API_KEY"
    echo "   Then run this script again."
    exit 0
fi

# Check if API key is set
if grep -q "zk_dev_your_api_key_here" .env; then
    echo "⚠️  Warning: ZERION_API_KEY in .env appears to be the example value"
    echo "   Please edit .env and set your actual API key"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo "🔨 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting Zerion MCP Server..."
docker-compose up -d

echo ""
echo "✅ Server is starting!"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🔍 Check status:"
echo "   docker-compose ps"
echo ""
echo "🛑 Stop server:"
echo "   docker-compose down"
echo ""
echo "📖 Full documentation: See DOCKER.md"
