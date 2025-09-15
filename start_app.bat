@echo off
echo Starting Plant Disease Detection PWA...
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :found
    )
)
:found

echo Local access: http://localhost:8504
echo Mobile access: http://%LOCAL_IP%:8504
echo.
echo To access from mobile:
echo 1. Connect mobile to same WiFi network
echo 2. Open browser and go to: http://%LOCAL_IP%:8504
echo 3. Look for 'Install App' button to install PWA
echo.

streamlit run main.py --server.address 0.0.0.0 --server.port 8504