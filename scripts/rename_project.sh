#!/bin/bash
# Script para renomear o diretório principal do projeto para RT-DETR

set -e

# Diretório atual
CURRENT_DIR="ObjectDetection_RT-DETRv2"
NEW_DIR="RT-DETR"

# Diretório pai
PARENT_DIR="/Users/ricardoguembarovski/Documents/Documentos_MacBook_Pro/Realtec/Buddmeyer/Automacao_Robo"

# Caminho completo
CURRENT_PATH="$PARENT_DIR/$CURRENT_DIR"
NEW_PATH="$PARENT_DIR/$NEW_DIR"

echo "======================================================================"
echo "🔄 RENOMEANDO PROJETO"
echo "======================================================================"
echo ""
echo "De: $CURRENT_DIR"
echo "Para: $NEW_DIR"
echo ""

# Verificar se diretório atual existe
if [ ! -d "$CURRENT_PATH" ]; then
    echo "❌ Erro: Diretório $CURRENT_PATH não encontrado!"
    exit 1
fi

# Verificar se novo diretório já existe
if [ -d "$NEW_PATH" ]; then
    echo "⚠️  Aviso: Diretório $NEW_PATH já existe!"
    read -p "Deseja continuar mesmo assim? (s/N): " resposta
    if [ "$resposta" != "s" ]; then
        echo "Operação cancelada."
        exit 0
    fi
fi

# Confirmar
read -p "Deseja continuar com a renomeação? (s/N): " resposta
if [ "$resposta" != "s" ]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "🔄 Renomeando diretório..."
cd "$PARENT_DIR"
mv "$CURRENT_DIR" "$NEW_DIR"

if [ $? -eq 0 ]; then
    echo "✅ Diretório renomeado com sucesso!"
    echo ""
    echo "📝 PRÓXIMOS PASSOS:"
    echo "1. Atualize seu ambiente de trabalho para usar o novo caminho"
    echo "2. Atualize variáveis de ambiente se necessário"
    echo "3. Teste o sistema para garantir que tudo funciona"
    echo ""
    echo "Novo caminho: $NEW_PATH"
else
    echo "❌ Erro ao renomear diretório!"
    exit 1
fi

