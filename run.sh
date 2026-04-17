#!/usr/bin/env bash

set -e

echo "🔧 Creating virtual environment..."

if [ ! -d "venv" ]; then
python3 -m venv venv
fi

echo "⚡ Activating virtual environment..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📦 Installing dependencies..."

if [ ! -f "requirements.txt" ]; then
echo "❌ requirements.txt not found!"
echo "Run this once: pip freeze > requirements.txt"
exit 1
fi

pip install -r requirements.txt

echo "🌐 Setting PYTHONPATH..."
export PYTHONPATH=$(pwd)/src

echo "🚀 Starting AgenticAIPlatform10..."
python3 src/platform10/main.py
