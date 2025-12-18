#!/bin/bash

set -e

echo "🚀 Configurando ambiente ObjectDetection_RT-DETR para Mac..."

# Criar venv se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar venv
echo "🔌 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Testar MPS
echo "🧪 Testando suporte MPS..."
python3 << EOF
import torch
import sys

print(f"PyTorch version: {torch.__version__}")
print(f"Python version: {sys.version}")

if torch.backends.mps.is_available():
    print("✅ MPS está disponível!")
    print(f"   MPS built: {torch.backends.mps.is_built()}")
    
    # Teste básico
    try:
        x = torch.randn(3, 3).to("mps")
        y = x * 2
        print("✅ Teste básico MPS passou!")
    except Exception as e:
        print(f"⚠️  Erro no teste MPS: {e}")
        print("   Considere habilitar PYTORCH_ENABLE_MPS_FALLBACK=1")
else:
    print("❌ MPS não está disponível")
    print("   Usando CPU como fallback")
    
print("\n✅ Setup concluído!")
EOF

echo ""
echo "✨ Ambiente configurado com sucesso!"
echo "   Para ativar o ambiente, execute: source .venv/bin/activate"

