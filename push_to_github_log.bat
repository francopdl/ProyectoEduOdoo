@echo off
setlocal enabledelayedexpansion

set "LOG_FILE=c:\Users\franc\OneDrive\Desktop\Odoo-Proyecto\odoo\addons\gestion_academy\git_push.log"

cd /d "c:\Users\franc\OneDrive\Desktop\Odoo-Proyecto\odoo\addons\gestion_academy" >"%LOG_FILE%" 2>&1

echo. >> "%LOG_FILE%"
echo ================================================== >> "%LOG_FILE%"
echo Subiendo gestion_academy a GitHub >> "%LOG_FILE%"
echo ================================================== >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Eliminar .git si existe
if exist .git (
    echo [1/9] Eliminando carpeta .git existente... >> "%LOG_FILE%"
    rmdir /s /q .git >> "%LOG_FILE%" 2>&1
    echo [OK] .git eliminado >> "%LOG_FILE%"
    echo. >> "%LOG_FILE%"
)

REM Inicializar repositorio
echo [2/9] Inicializando repositorio git... >> "%LOG_FILE%"
call git init >> "%LOG_FILE%" 2>&1
echo [OK] Repositorio inicializado >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Configurar usuario
echo [3/9] Configurando usuario git... >> "%LOG_FILE%"
call git config user.name "Franco" >> "%LOG_FILE%" 2>&1
call git config user.email "franco@example.com" >> "%LOG_FILE%" 2>&1
echo [OK] Usuario configurado >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Añadir archivos
echo [4/9] Añadiendo archivos... >> "%LOG_FILE%"
call git add . >> "%LOG_FILE%" 2>&1
echo [OK] Archivos añadidos >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Commit
echo [5/9] Haciendo commit inicial... >> "%LOG_FILE%"
call git commit -m "Initial commit: gestion_academy module" >> "%LOG_FILE%" 2>&1
echo [OK] Commit realizado >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Rama main
echo [6/9] Cambiando a rama 'main'... >> "%LOG_FILE%"
call git branch -M main >> "%LOG_FILE%" 2>&1
echo [OK] Rama cambiada a main >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Remote
echo [7/9] Añadiendo remote origin... >> "%LOG_FILE%"
call git remote add origin https://github.com/francopdl/ProyectoEduOdoo.git >> "%LOG_FILE%" 2>&1
echo [OK] Remote añadido >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Verificar
echo [8/9] Verificando configuracion... >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"
echo Ramas: >> "%LOG_FILE%"
call git branch -a >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"
echo Remotes: >> "%LOG_FILE%"
call git remote -v >> "%LOG_FILE%" 2>&1
echo. >> "%LOG_FILE%"

REM Push
echo [9/9] Haciendo push a GitHub... >> "%LOG_FILE%"
call git push -u origin main --force >> "%LOG_FILE%" 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Falló el push. Ver detalles arriba. >> "%LOG_FILE%"
) else (
    echo [SUCCESS] Push completado! >> "%LOG_FILE%"
)
echo. >> "%LOG_FILE%"
echo ================================================== >> "%LOG_FILE%"
echo Proceso finalizado >> "%LOG_FILE%"
echo ================================================== >> "%LOG_FILE%"

echo Script ejecutado. Revisa el log en: %LOG_FILE%
type "%LOG_FILE%"
pause
