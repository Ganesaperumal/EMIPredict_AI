#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Activate the virtual environment if it exists
if [ -d "venv" ]; then
    echo "✅ Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️ Warning: venv folder not found. Running with global python..."
fi

# Run the Streamlit app
# --server.headless=false ensures it tries to open the browser automatically
echo "🚀 Starting EMI Predict AI..."
streamlit run app.py --server.headless=false
