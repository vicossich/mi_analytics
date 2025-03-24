@echo off
REM === Define paths ===
SET NSSM_PATH=D:\nssm-2.24\win64\nssm.exe
SET PROJECT_PATH=D:\mi_analytics
SET PYTHON_PATH=%PROJECT_PATH%\venv\Scripts\python.exe
SET SCRIPT_NAME=main.py
SET LOG_DIR=%PROJECT_PATH%\logs

REM === Define service name ===
SET SERVICE_NAME=mi_analytics

REM === Create logs folder if it doesn't exist ===
IF NOT EXIST "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

REM === Remove existing service (if any) ===
echo Removing existing service (if it exists)...
%NSSM_PATH% remove %SERVICE_NAME% confirm

REM === Create new service ===
echo Creating new service: %SERVICE_NAME%
%NSSM_PATH% install %SERVICE_NAME% %PYTHON_PATH% -m streamlit run %SCRIPT_NAME%
%NSSM_PATH% set %SERVICE_NAME% AppDirectory %PROJECT_PATH%
%NSSM_PATH% set %SERVICE_NAME% StartDirectory %PROJECT_PATH%
%NSSM_PATH% set %SERVICE_NAME% AppRestartDelay 5000
%NSSM_PATH% set %SERVICE_NAME% AppStdout %LOG_DIR%\stdout.log
%NSSM_PATH% set %SERVICE_NAME% AppStderr %LOG_DIR%\stderr.log
%NSSM_PATH% set %SERVICE_NAME% AppRotateFiles 1
%NSSM_PATH% set %SERVICE_NAME% AppRotateOnline 1

REM === Start the service ===
echo Starting the service...
net start %SERVICE_NAME%

echo.
echo Service "%SERVICE_NAME%" has been successfully installed and started!
pause
