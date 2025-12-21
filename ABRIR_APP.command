#!/bin/bash
# Script para abrir o app ObjectDetection_RT-DETR
# Clique duas vezes neste arquivo para executar

cd "$(dirname "$0")"

echo "🚀 Abrindo ObjectDetection_RT-DETR..."
echo ""

# Tentar abrir o app
if [ -d "dist/ObjectDetection_RT-DETR.app" ]; then
    open dist/ObjectDetection_RT-DETR.app
    echo "✅ App aberto!"
elif [ -d "ObjectDetection_RT-DETR.app" ]; then
    open ObjectDetection_RT-DETR.app
    echo "✅ App aberto!"
else
    echo "❌ App não encontrado!"
    echo "   Execute: ./create_executable.sh para criar o executável"
    read -p "Pressione Enter para sair..."
fi

