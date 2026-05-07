@echo off
title Kiosque Rental
color 0A

echo.
echo  ============================================
echo    KIOSQUE RENTAL — Sistema de Reservas
echo  ============================================
echo.

:: ── Verifica Python ──────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python nao encontrado!
    echo  Instale em: https://python.org
    pause & exit /b
)

:: ── Instala Flask se necessario ──────────────
echo  Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo  Instalando Flask...
    pip install flask --quiet
)
echo  Flask OK.
echo.

:: ── Informa estrutura ────────────────────────
echo  Iniciando servidores...
echo.
echo  BACKEND  ^> http://localhost:5000
echo  LOGIN    ^> usuario: 123  /  senha: 123
echo.
echo  Feche as janelas abertas para encerrar.
echo  ============================================
echo.

:: ── Abre terminal do BACKEND ─────────────────
start "KIOSQUE — Backend (Flask)" cmd /k "cd /d "%~dp0src" && echo [BACKEND] Iniciando Flask... && python app.py"

:: ── Aguarda 2s para o Flask subir ────────────
timeout /t 2 /nobreak >nul

:: ── Abre o navegador ─────────────────────────
start "" "http://localhost:5000"

echo  Servidores iniciados! Verifique as janelas abertas.
echo.
pause
