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

echo Laptop access: http://localhost:8501
echo Mobile access: http://%LOCAL_IP%:8501
echo.

streamlit run main.py