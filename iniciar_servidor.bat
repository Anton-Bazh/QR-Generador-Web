@echo off
title Servidor Generador QR
cls

echo ========================================================
echo   Iniciando Servidor Web QR para Windows Server
echo ========================================================
echo.

echo [1/3] Verificando dependencias...
call pip install -r requirements.txt >nul 2>&1
call pip install waitress >nul 2>&1
echo - Dependencias instaladas y actualizadas correctamente.
echo.

echo [2/3] Tu panel estara disponible en la direccion IP de este equipo:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| find "IPv4"') do echo  - %%a:5000
echo.

echo [3/3] Arrancando servidor de produccion en el puerto 5000...
echo.
echo ========================================================
echo El servidor esta ejecutandose. No cierres esta ventana.
echo Para apagar el servidor de forma segura, presiona CTRL+C
echo ========================================================
echo.

python -c "from waitress import serve; from app import create_app; app = create_app(); serve(app, host='0.0.0.0', port=5000)"

pause
