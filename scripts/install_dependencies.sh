#!/bin/bash

# Script para instalar dependências do projeto ObjectDetection_RT-DETR

set -e

echo "📦 Instalando dependências do ObjectDetection_RT-DETR..."
echo ""

# Verificar se está em ambiente virtual ou conda
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo "✅ Ambiente conda detectado: $CONDA_DEFAULT_ENV"
    PIP_CMD="pip"
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Ambiente virtual detectado: $VIRTUAL_ENV"
    PIP_CMD="pip"
else
    echo "⚠️  Nenhum ambiente virtual detectado!"
    echo "   Recomendado: source .venv/bin/activate ou conda activate seu_ambiente"
    read -p "Continuar mesmo assim? (s/N): " resposta
    if [ "$resposta" != "s" ]; then
        echo "Operação cancelada."
        exit 1
    fi
    PIP_CMD="pip3"
fi

echo ""
echo "📥 Instalando pacotes do requirements.txt..."
$PIP_CMD install -r requirements.txt

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "📋 Verificando instalação..."
python -c "import torch; print(f'  ✅ PyTorch: {torch.__version__}')" 2>/dev/null || echo "  ❌ PyTorch não encontrado"
python -c "import transformers; print(f'  ✅ Transformers: {transformers.__version__}')" 2>/dev/null || echo "  ❌ Transformers não encontrado"
python -c "import roboflow; print(f'  ✅ Roboflow: {roboflow.__version__}')" 2>/dev/null || echo "  ❌ Roboflow não encontrado"
python -c "import pycocotools; print('  ✅ pycocotools instalado')" 2>/dev/null || echo "  ❌ pycocotools não encontrado"

echo ""
echo "✨ Pronto para usar!"

