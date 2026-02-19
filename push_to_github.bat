@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\franc\OneDrive\Desktop\Odoo-Proyecto\odoo\addons\gestion_academy"

echo.
echo ================================================
echo Subiendo gestion_academy a GitHub
echo ================================================
echo.

REM Eliminar .git si existe
if exist .git (
    echo [1] Eliminando carpeta .git existente...
    rmdir /s /q .git
    echo [OK] .git eliminado
    echo.
)

REM Inicializar repositorio
echo [2] Inicializando repositorio git...
git init
if !errorlevel! neq 0 (
    echo [ERROR] Falló al inicializar git
    exit /b 1
)
echo [OK] Repositorio inicializado
echo.

REM Configurar usuario
echo [3] Configurando usuario git...
git config user.name "Franco"
git config user.email "franco@example.com"
echo [OK] Usuario configurado
echo.

REM Añadir archivos
echo [4] Añadiendo archivos...
git add .
if !errorlevel! neq 0 (
    echo [ERROR] Falló al añadir archivos
    exit /b 1
)
echo [OK] Archivos añadidos
echo.

REM Commit inicial
echo [5] Haciendo commit inicial...
git commit -m "Initial commit: gestion_academy module"
if !errorlevel! neq 0 (
    echo [ERROR] Falló al hacer commit
    exit /b 1
)
echo [OK] Commit realizado
echo.

REM Cambiar a rama main
echo [6] Cambiando a rama 'main'...
git branch -M main
echo [OK] Rama cambiada a main
echo.

REM Añadir remote
echo [7] Añadiendo remote origin...
git remote add origin https://github.com/francopdl/ProyectoEduOdoo.git
if !errorlevel! neq 0 (
    echo [ERROR] Falló al añadir remote
    exit /b 1
)
echo [OK] Remote añadido
echo.

REM Verificar estado
echo [8] Estado actual del repositorio:
echo.
echo Configuracion git:
git config --local -l
echo.
echo Ramas:
git branch -a
echo.
echo Remotes:
git remote -v
echo.

REM Push a GitHub
echo [9] Haciendo push a GitHub (main --force)...
git push -u origin main --force
if !errorlevel! neq 0 (
    echo [ERROR] Falló al hacer push
    echo Posible causa: Credenciales de GitHub incorrectas o sin permisos
    exit /b 1
)
echo [OK] Push completado exitosamente!
echo.

echo ================================================
echo [SUCCESS] Proyecto subido a GitHub!
echo ================================================
pause
