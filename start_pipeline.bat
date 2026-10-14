```bat
@echo off
setlocal EnableExtensions

title Earthquake Intelligence Pipeline Launcher

REM ==========================================
REM Project and service paths
REM ==========================================
set "PROJECT_DIR=C:\Users\HP\OneDrive\Desktop\Real-Time-Earthquake-Inteligence-System"
set "KAFKA_DIR=C:\kafka"
set "MINIO_DIR=C:\minio"
set "MINIO_DATA=C:\minio-data"
set "VENV_ACTIVATE=%PROJECT_DIR%\venv\Scripts\activate.bat"

echo.
echo ==========================================
echo  REAL-TIME EARTHQUAKE INTELLIGENCE SYSTEM
echo ==========================================
echo.

REM ==========================================
REM Validate paths
REM ==========================================
if not exist "%PROJECT_DIR%\src\earthquake_producer.py" (
    echo ERROR: earthquake_producer.py not found.
    echo Check PROJECT_DIR in this BAT file.
    pause
    exit /b 1
)

if not exist "%PROJECT_DIR%\src\stream_pipeline.py" (
    echo ERROR: stream_pipeline.py not found.
    pause
    exit /b 1
)

if not exist "%VENV_ACTIVATE%" (
    echo ERROR: Python virtual environment not found:
    echo %VENV_ACTIVATE%
    pause
    exit /b 1
)

REM ==========================================
REM STEP 1: Start Kafka
REM ==========================================
echo [1/5] Starting Kafka service...

powershell -NoProfile -Command "if (Test-NetConnection localhost -Port 9092 -InformationLevel Quiet) { exit 0 } else { exit 1 }"

if errorlevel 1 (
    start "Kafka Broker" cmd /k "cd /d ""%KAFKA_DIR%"" && .\bin\windows\kafka-server-start.bat .\config\server.properties"
) else (
    echo Kafka is already running.
)

echo Waiting for Kafka on port 9092...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$deadline=(Get-Date).AddSeconds(90); do { Start-Sleep -Seconds 2; $ready=Test-NetConnection localhost -Port 9092 -InformationLevel Quiet } until ($ready -or (Get-Date) -ge $deadline); if (-not $ready) { exit 1 }"

if errorlevel 1 (
    echo ERROR: Kafka did not start within 90 seconds.
    pause
    exit /b 1
)

echo Kafka is ready.
echo.

REM ==========================================
REM STEP 2: Start MinIO
REM ==========================================
echo [2/5] Starting MinIO service...

powershell -NoProfile -Command "if (Test-NetConnection localhost -Port 9000 -InformationLevel Quiet) { exit 0 } else { exit 1 }"

if errorlevel 1 (
    start "MinIO Server" cmd /k "cd /d ""%MINIO_DIR%"" && minio.exe server ""%MINIO_DATA%"" --console-address "":9001"""
) else (
    echo MinIO is already running.
)

echo Waiting for MinIO on port 9000...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$deadline=(Get-Date).AddSeconds(60); do { Start-Sleep -Seconds 2; $ready=Test-NetConnection localhost -Port 9000 -InformationLevel Quiet } until ($ready -or (Get-Date) -ge $deadline); if (-not $ready) { exit 1 }"

if errorlevel 1 (
    echo ERROR: MinIO did not start within 60 seconds.
    pause
    exit /b 1
)

echo MinIO is ready.
echo Console: http://localhost:9001
echo.

REM ==========================================
REM STEP 3: Start Earthquake Producer
REM ==========================================
echo [3/5] Starting Earthquake Producer...

start "Earthquake Producer" cmd /k "cd /d ""%PROJECT_DIR%"" && call venv\Scripts\activate.bat && python -m src.earthquake_producer"

echo Waiting for producer to create the Kafka topic...

REM Wait up to 60 seconds for earthquake-events topic
powershell -NoProfile -ExecutionPolicy Bypass -Command "$deadline=(Get-Date).AddSeconds(60); do { Start-Sleep -Seconds 3; $topics = & '%KAFKA_DIR%\bin\windows\kafka-topics.bat' --bootstrap-server localhost:9092 --list 2>$null; $ready = $topics -contains 'earthquake-events' } until ($ready -or (Get-Date) -ge $deadline); if (-not $ready) { exit 1 }"

if errorlevel 1 (
    echo WARNING: Could not confirm earthquake-events topic.
    echo Check the Earthquake Producer terminal before proceeding.
    pause
)

echo Producer topic check completed.
echo.

REM ==========================================
REM STEP 4: Start Spark Streaming Pipeline
REM ==========================================
echo [4/5] Starting Spark Stream Pipeline...

start "Earthquake Stream Pipeline" cmd /k "cd /d ""%PROJECT_DIR%"" && call venv\Scripts\activate.bat && python -m src.stream_pipeline"

echo.
echo [5/5] Startup commands completed.
echo.
echo ==========================================
echo  SERVICES STARTED
echo ==========================================
echo Kafka:       localhost:9092
echo MinIO API:   http://localhost:9000
echo MinIO UI:    http://localhost:9001
echo Kafka topic: earthquake-events
echo.
echo Keep all service terminals open.
echo To stop the pipeline, stop each service window.
echo.
pause
```
