#!/bin/bash
# Script simplificado para criar executável rapidamente

set -e

echo "🚀 Criando executável ObjectDetection_RT-DETR..."
echo "================================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 não encontrado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python: $PYTHON_VERSION"
echo ""

# Verificar se PyInstaller está instalado
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "📦 PyInstaller não encontrado. Instalando..."
    python3 -m pip install --upgrade pip
    python3 -m pip install pyinstaller
    echo "✅ PyInstaller instalado!"
    echo ""
fi

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf build dist *.spec 2>/dev/null || true

# Criar executável
echo "🔨 Criando executável (isso pode levar alguns minutos)..."
echo ""

python3 -m PyInstaller \
    --name="ObjectDetection_RT-DETR" \
    --onedir \
    --noconfirm \
    --console \
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
    --hidden-import="src.utils.executable_paths" \
    --hidden-import="transformers.models.rtdetr" \
    --hidden-import="transformers.models.rtdetr.modeling_rtdetr" \
    --hidden-import="transformers.models.rtdetr.configuration_rtdetr" \
    --hidden-import="transformers.models.rtdetr.image_processing_rtdetr" \
    --hidden-import="torch" \
    --hidden-import="cv2" \
    --hidden-import="PIL" \
    --hidden-import="PIL.Image" \
    --hidden-import="PIL.ImageTk" \
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
    --exclude-module="transformers.tests" \
    app.py

# Verificar se foi criado (onedir cria uma pasta)
if [ -d "dist/ObjectDetection_RT-DETR" ]; then
    EXECUTABLE_PATH="dist/ObjectDetection_RT-DETR/ObjectDetection_RT-DETR"
    
    if [ -f "$EXECUTABLE_PATH" ]; then
        echo ""
        echo "✅ Executável criado com sucesso!"
        chmod +x "$EXECUTABLE_PATH"
        
        # Criar bundle .app compatível com macOS moderno
        echo "📦 Criando bundle .app compatível com macOS 15+..."
        
        APP_NAME="ObjectDetection_RT-DETR.app"
        APP_PATH="dist/$APP_NAME"
        
        # Remover bundle antigo se existir
        rm -rf "$APP_PATH"
        
        # Criar estrutura do bundle
        mkdir -p "$APP_PATH/Contents/MacOS"
        mkdir -p "$APP_PATH/Contents/Resources"
        
        # Copiar TODOS os arquivos do diretório dist/ObjectDetection_RT-DETR para o bundle
        # O PyInstaller precisa de todos os arquivos no mesmo local relativo
        if [ -d "dist/ObjectDetection_RT-DETR" ]; then
            # Copiar TODO o conteúdo (incluindo _internal, Frameworks, etc.) para Resources
            cp -r dist/ObjectDetection_RT-DETR/* "$APP_PATH/Contents/Resources/" 2>/dev/null || true
            
            # Criar script wrapper que executa o executável do local correto
            cat > "$APP_PATH/Contents/MacOS/ObjectDetection_RT-DETR" << 'WRAPPER'
#!/bin/bash
# Wrapper script para executar o app com caminhos corretos

# Obter diretório do app (Contents/MacOS -> Contents -> raiz do app)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
RESOURCES_DIR="$APP_DIR/Resources"

# Verificar se Resources existe
if [ ! -d "$RESOURCES_DIR" ]; then
    osascript -e 'display dialog "Erro: Diretório Resources não encontrado!" buttons {"OK"} default button "OK" with icon stop' 2>/dev/null
    exit 1
fi

# Verificar se executável existe
if [ ! -f "$RESOURCES_DIR/ObjectDetection_RT-DETR" ]; then
    osascript -e 'display dialog "Erro: Executável não encontrado!" buttons {"OK"} default button "OK" with icon stop' 2>/dev/null
    exit 1
fi

# Mudar para o diretório Resources onde estão os arquivos
cd "$RESOURCES_DIR"

# Executar o executável real (que está em Resources)
exec "$RESOURCES_DIR/ObjectDetection_RT-DETR" "$@"
WRAPPER
            chmod +x "$APP_PATH/Contents/MacOS/ObjectDetection_RT-DETR"
        else
            # Fallback: copiar apenas o executável
            cp "$EXECUTABLE_PATH" "$APP_PATH/Contents/MacOS/ObjectDetection_RT-DETR"
            chmod +x "$APP_PATH/Contents/MacOS/ObjectDetection_RT-DETR"
        fi
        
        # Criar Info.plist compatível com macOS moderno (sem Carbon)
        cat > "$APP_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>ObjectDetection RT-DETR</string>
    <key>CFBundleExecutable</key>
    <string>ObjectDetection_RT-DETR</string>
    <key>CFBundleIdentifier</key>
    <string>com.realtec.ObjectDetection-RT-DETR</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>ObjectDetection_RT-DETR</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
</dict>
</plist>
EOF
        
        echo "✅ Bundle .app criado: $APP_PATH"
        echo ""
        echo "📍 Localização: $(pwd)/$APP_PATH"
        echo ""
        echo "📋 Para executar:"
        echo "   open $APP_PATH"
        echo "   ou"
        echo "   ./$APP_PATH/Contents/MacOS/ObjectDetection_RT-DETR"
        echo ""
        echo "💡 Ou clique duas vezes no arquivo no Finder"
        
        # Criar link simbólico no diretório raiz
        if [ ! -L "$APP_NAME" ] && [ ! -d "$APP_NAME" ]; then
            ln -s "$(pwd)/$APP_PATH" "$(pwd)/$APP_NAME"
            echo "✅ Link simbólico criado: $(pwd)/$APP_NAME"
        fi
    else
        echo "❌ Erro: Executável não encontrado em $EXECUTABLE_PATH"
        exit 1
    fi
else
    echo "❌ Erro: Executável não foi criado"
    exit 1
fi

