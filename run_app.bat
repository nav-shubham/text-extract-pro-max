@echo off
:: Navigate to this script's directory
cd /d "%~dp0"

echo [SYSTEM] Starting Upgraded TextExtract Pro Max v7.0...
echo [SYSTEM] Launching Streamlit inside Rust-powered 'uv' project environment...
echo [SYSTEM] Press Ctrl+C in this terminal window to stop the server.
echo.

uv run streamlit run main.py

pause
