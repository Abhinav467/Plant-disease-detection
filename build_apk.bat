@echo off
echo Installing Buildozer...
pip install buildozer

echo Setting up Android SDK...
buildozer android debug

echo APK will be created in bin/ folder
pause