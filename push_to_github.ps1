# Script para subir gestion_academy a GitHub
$scriptPath = $PSScriptRoot
Write-Host "Navegando a: $scriptPath" -ForegroundColor Green

# Cambiar al directorio del módulo
Set-Location $scriptPath

# Verificar si existe .git y eliminarlo
if (Test-Path .git) {
    Write-Host "Eliminando carpeta .git existente..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .git
    Write-Host ".git eliminado" -ForegroundColor Green
}

# Inicializar repositorio git
Write-Host "Inicializando repositorio git..." -ForegroundColor Green
git init

# Configurar usuario
Write-Host "Configurando usuario git..." -ForegroundColor Green
git config user.name "Franco"
git config user.email "franco@example.com"

# Añadir todos los archivos
Write-Host "Añadiendo todos los archivos..." -ForegroundColor Green
git add .

# Hacer commit inicial
Write-Host "Haciendo commit inicial..." -ForegroundColor Green
git commit -m "Initial commit: gestion_academy module"

# Cambiar a rama main
Write-Host "Cambiando a rama 'main'..." -ForegroundColor Green
git branch -M main

# Añadir remote
Write-Host "Añadiendo remote origin..." -ForegroundColor Green
git remote add origin https://github.com/francopdl/ProyectoEduOdoo.git

# Verificar configuración
Write-Host "`nConfiguracion actual:" -ForegroundColor Cyan
git config --local -l
Write-Host "`nRamas:" -ForegroundColor Cyan
git branch -a
Write-Host "`nRemotes:" -ForegroundColor Cyan
git remote -v

# Hacer push a GitHub
Write-Host "`nHaciendo push a GitHub..." -ForegroundColor Green
try {
    git push -u origin main --force
    Write-Host "Push completado exitosamente!" -ForegroundColor Green
}
catch {
    Write-Host "Error al hacer push: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nProyecto subido exitosamente a GitHub!" -ForegroundColor Green
