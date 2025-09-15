@echo off
echo Getting your IP address for mobile access...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo.
        echo Mobile URL: http://%%b:8501
        echo.
        goto :start
    )
)
:start
echo Starting PWA with mobile access...
streamlit run main.py --server.address 0.0.0.0 --server.port 8501