#!/bin/bash

cd "/c/Users/franc/OneDrive/Desktop/Odoo-Proyecto/odoo/addons/gestion_academy"

echo "=========================================="
echo "Subiendo gestion_academy a GitHub"
echo "=========================================="
echo ""

# Eliminar .git si existe
echo "[1] Eliminando carpeta .git existente..."
if [ -d ".git" ]; then
    rm -rf .git
    echo "[OK] .git eliminado"
else
    echo "[INFO] No existe carpeta .git previa"
fi
echo ""

# Inicializar repositorio
echo "[2] Inicializando repositorio git..."
git init
echo "[OK] Repositorio inicializado"
echo ""

# Configurar usuario
echo "[3] Configurando usuario git..."
git config user.name "Franco"
git config user.email "franco@example.com"
echo "[OK] Usuario configurado"
echo ""

# Añadir archivos
echo "[4] Añadiendo archivos..."
git add .
echo "[OK] Archivos añadidos"
echo ""

# Commit inicial
echo "[5] Haciendo commit inicial..."
git commit -m "Initial commit: gestion_academy module"
echo "[OK] Commit realizado"
echo ""

# Cambiar a rama main
echo "[6] Cambiando a rama 'main'..."
git branch -M main
echo "[OK] Rama cambiada a main"
echo ""

# Añadir remote
echo "[7] Añadiendo remote origin..."
git remote add origin https://github.com/francopdl/ProyectoEduOdoo.git
echo "[OK] Remote añadido"
echo ""

# Verificar estado
echo "[8] Estado actual:"
echo ""
echo "Ramas:"
git branch -a
echo ""
echo "Remotes:"
git remote -v
echo ""

# Push a GitHub
echo "[9] Haciendo push a GitHub..."
git push -u origin main --force
echo "[OK] Push completado"
echo ""

echo "=========================================="
echo "[SUCCESS] Proyecto subido a GitHub!"
echo "=========================================="
