#!/bin/bash

echo "🚀 Starting WhatsApp Bulk Messenger..."
echo "============================================"

# Check if virtual environment exists
if [ ! -d "whatsapp_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv whatsapp_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source whatsapp_env/bin/activate

# Install dependencies if not already installed
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Start the Streamlit app
echo "🌐 Starting web application..."
echo "The app will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo "============================================"

streamlit run app.py