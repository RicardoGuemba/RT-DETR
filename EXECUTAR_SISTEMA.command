#!/bin/bash
# Script para executar o sistema ObjectDetection_RT-DETR
# Clique duas vezes neste arquivo para executar o sistema

cd "$(dirname "$0")"

# Verificar se existe executável
if [ -d "dist/ObjectDetection_RT-DETR.app" ]; then
    echo "🚀 Iniciando ObjectDetection_RT-DETR..."
    open dist/ObjectDetection_RT-DETR.app
elif [ -f "dist/ObjectDetection_RT-DETR/ObjectDetection_RT-DETR" ]; then
    echo "🚀 Iniciando ObjectDetection_RT-DETR..."
    ./dist/ObjectDetection_RT-DETR/ObjectDetection_RT-DETR
elif [ -f "dist/ObjectDetection_RT-DETR" ]; then
    echo "🚀 Iniciando ObjectDetection_RT-DETR..."
    ./dist/ObjectDetection_RT-DETR
elif [ -f "app.py" ]; then
    echo "🚀 Executável não encontrado. Executando via Python..."
    python3 app.py
else
    echo "❌ Erro: Não foi possível encontrar o executável ou app.py"
    echo "   Execute: ./create_executable.sh para criar o executável"
    read -p "Pressione Enter para sair..."
fi

