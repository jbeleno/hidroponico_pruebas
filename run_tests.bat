@echo off
REM Script para ejecutar las pruebas del sistema hidropónico en Windows

echo 🧪 Ejecutando pruebas del Sistema Hidropónico
echo ==============================================
echo.

REM Verificar que pytest está instalado
where pytest >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pytest no está instalado. Instalando dependencias...
    pip install -r requirements.txt
)

REM Verificar que los servicios están corriendo
echo 📋 Verificando servicios...
docker-compose ps | findstr "hidroponico_backend.*Up" >nul
if %errorlevel% neq 0 (
    echo ⚠️  El backend no está corriendo. Iniciando servicios...
    docker-compose up -d
    echo ⏳ Esperando a que los servicios estén listos...
    timeout /t 5 /nobreak >nul
)

REM Menú de opciones
echo.
echo Selecciona el tipo de pruebas a ejecutar:
echo 1) Todas las pruebas
echo 2) Solo pruebas unitarias
echo 3) Solo pruebas de integración
echo 4) Pruebas con cobertura
echo 5) Salir
echo.
set /p option="Opción: "

if "%option%"=="1" (
    echo.
    echo 🚀 Ejecutando todas las pruebas...
    pytest tests/ -v
) else if "%option%"=="2" (
    echo.
    echo 🔬 Ejecutando pruebas unitarias...
    pytest tests/ -m unit -v
) else if "%option%"=="3" (
    echo.
    echo 🌐 Ejecutando pruebas de integración...
    pytest tests/ -m integration -v
) else if "%option%"=="4" (
    echo.
    echo 📊 Ejecutando pruebas con cobertura...
    pytest tests/ --cov=backend --cov-report=html --cov-report=term
    echo.
    echo ✅ Reporte de cobertura generado en htmlcov\index.html
) else if "%option%"=="5" (
    echo 👋 Saliendo...
    exit /b 0
) else (
    echo ❌ Opción inválida
    exit /b 1
)

echo.
echo ✅ Pruebas completadas

