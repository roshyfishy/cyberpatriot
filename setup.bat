@echo off
setlocal

set LOGFILE=%USERPROFILE%\Downloads\CyberPatriot\setup.log
set PYTHON_SCRIPT=%USERPROFILE%\Downloads\CyberPatriot\windows\launcher.py

echo [%DATE% %TIME%] setup start >> "%LOGFILE%"

echo [%DATE% %TIME%] checking for administrative permissions... >> "%LOGFILE%"
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [%DATE% %TIME%] requesting administrative privileges... >> "%LOGFILE%"
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
echo [%DATE% %TIME%] success! >> "%LOGFILE%"

echo [%DATE% %TIME%] installing python... >> "%LOGFILE%"
where python >nul 2>&1
if %errorlevel%==0 (
    echo [%DATE% %TIME%] Python is already installed. >> "%LOGFILE%"
) else (
    set PYTHON_URL=https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe
    curl -o "python-installer.exe" "%PYTHON_URL%"
    "python-installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del "python-installer.exe"
    echo [%DATE% %TIME%] Python has been installed. >> "%LOGFILE%"
)

echo [%DATE% %TIME%] running Python script... >> "%LOGFILE%"
python "%PYTHON_SCRIPT%"
echo [%DATE% %TIME%] Python script completed! >> "%LOGFILE%"

exit /b 0