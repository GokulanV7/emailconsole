#!/bin/bash

# Gmail Interactive Client Installation Script

echo "🚀 Gmail Interactive Client Installation"
echo "======================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [[ $(echo "$python_version >= $required_version" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.8+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Make CLI launcher executable
echo "🔗 Setting up CLI launcher..."
chmod +x gmail-client

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🎯 Quick Start:"
echo "  1. Run: source venv/bin/activate"
echo "  2. Run: ./gmail-client"
echo "     or: python main.py"
echo ""
echo "📋 System-wide installation (optional):"
echo "  pip install -e ."
echo "  Then run: gmail-client (from anywhere)"
echo ""
echo "🔐 Security Note:"
echo "  The application will prompt for your Gmail credentials at startup."
echo "  Use Gmail App Passwords for enhanced security."
echo ""
echo "📚 For more options, see INSTALL.md"
