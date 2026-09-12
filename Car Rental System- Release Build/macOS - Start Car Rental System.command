#!/bin/bash
cd "$(dirname "$0")/Car_Rental_System" || exit 1

if command -v python3 >/dev/null 2>&1; then
    exec python3 main.py
elif command -v python >/dev/null 2>&1; then
    exec python main.py
else
    echo ""
    echo "Python 3 is required to run Car Rental System."
    echo "Install Python 3 from https://www.python.org/downloads/"
    echo ""
    read -r -p "Press Enter to close..."
    exit 1
fi
