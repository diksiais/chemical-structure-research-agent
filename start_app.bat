@echo off
setlocal

:: Paths
set "CERTIFI_PATH=C:\Users\balis\AppData\Local\Programs\Python\Python313\Lib\site-packages\certifi\cacert.pem"
set "CUSTOM_CERT=C:\Users\balis\chemical_research_agent\custom_cert.pem"
set "BACKUP_PATH=%CERTIFI_PATH%.bak"

echo Checking certifi path...
if not exist "%CERTIFI_PATH%" (
    echo ❌ certifi not found at %CERTIFI_PATH%
    goto :run_app
)

if not exist "%CUSTOM_CERT%" (
    echo ⚠️ Custom certificate not found at %CUSTOM_CERT%
    goto :run_app
)

if not exist "%BACKUP_PATH%" (
    echo Creating backup of certifi cacert.pem...
    copy "%CERTIFI_PATH%" "%BACKUP_PATH%" > nul
)

:: Check if already appended
findstr /c:"# Custom Proxy Certificate" "%CERTIFI_PATH%" > nul
if errorlevel 1 (
    echo Appending custom certificate...
    (
        echo.
        echo # Custom Proxy Certificate
        type "%CUSTOM_CERT%"
    ) >> "%CERTIFI_PATH%"
) else (
    echo Custom certificate already appended.
)

:run_app
echo Starting Streamlit app...
cd /d C:\Users\balis\chemical_research_agent
call venv\Scripts\activate

if exist "venv\Scripts\streamlit.exe" (
    venv\Scripts\streamlit.exe run app.py
) else (
    echo ❌ Streamlit not found in virtual environment. Did you install it?
)

pause
