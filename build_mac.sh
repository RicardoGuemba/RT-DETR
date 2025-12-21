#!/bin/bash
# Script para criar executável macOS do ObjectDetection_RT-DETR

set -e  # Parar em caso de erro

echo "🍎 Criando executável para macOS..."
echo "=================================="
echo ""

# Verificar se estamos no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Erro: Este script deve ser executado no macOS"
    exit 1
fi

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não encontrado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python encontrado: $PYTHON_VERSION"

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependências específicas do Mac
echo "📦 Instalando dependências para macOS..."
pip install -r requirements-mac.txt

# Verificar PyInstaller
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Instalando PyInstaller..."
    pip install pyinstaller
fi

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build dist *.spec 2>/dev/null || true

# Criar executável
echo "🔨 Criando executável..."
pyinstaller \
    --name="ObjectDetection_RT-DETR" \
    --onefile \
    --windowed \
    --add-data "config:config" \
    --add-data "src:src" \
    --add-data "data:data" \
    --hidden-import="interface_tkinter" \
    --hidden-import="src.train_rtdetr" \
    --hidden-import="src.infer_images" \
    --hidden-import="src.infer_video" \
    --hidden-import="src.eval_coco" \
    --hidden-import="src.hf_model_utils" \
    --hidden-import="src.coco_utils" \
    --hidden-import="src.utils.paths" \
    --hidden-import="transformers.models.rtdetr" \
    --hidden-import="torch" \
    --hidden-import="cv2" \
    --hidden-import="PIL" \
    --hidden-import="pycocotools" \
    --hidden-import="roboflow" \
    --hidden-import="matplotlib.backends.backend_tkagg" \
    --collect-all="torch" \
    --collect-all="transformers" \
    --collect-all="cv2" \
    --exclude-module="matplotlib.tests" \
    --exclude-module="numpy.tests" \
    --exclude-module="scipy.tests" \
    --exclude-module="torch.test" \
    app.py

# Verificar se o executável foi criado
if [ -f "dist/ObjectDetection_RT-DETR" ]; then
    echo ""
    echo "✅ Executável criado com sucesso!"
    echo "📍 Localização: dist/ObjectDetection_RT-DETR"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Teste o executável: ./dist/ObjectDetection_RT-DETR"
    echo "   2. Se funcionar, você pode distribuir o arquivo"
    echo "   3. Para criar um .app bundle, execute: ./create_mac_app.sh"
    echo ""
else
    echo "❌ Erro: Executável não foi criado"
    exit 1
fi

