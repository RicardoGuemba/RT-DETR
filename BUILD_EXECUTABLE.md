# 📦 Guia para Criar Executáveis - ObjectDetection_RT-DETR

Este guia explica como criar executáveis independentes do sistema para macOS e Windows.

## 📋 Pré-requisitos

### macOS
- macOS 10.15 (Catalina) ou superior
- Python 3.8 ou superior
- Xcode Command Line Tools: `xcode-select --install`

### Windows
- Windows 10 ou superior
- Python 3.8 ou superior
- Visual C++ Redistributable (geralmente já instalado)

## 🍎 Criando Executável para macOS

### Método 1: Script Automatizado (Recomendado)

```bash
# Dar permissão de execução
chmod +x build_mac.sh

# Executar script
./build_mac.sh
```

O script irá:
1. Criar ambiente virtual
2. Instalar dependências específicas do macOS
3. Criar executável usando PyInstaller
4. Gerar arquivo em `dist/ObjectDetection_RT-DETR`

### Método 2: Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements-mac.txt

# 3. Instalar PyInstaller
pip install pyinstaller

# 4. Criar executável
pyinstaller --name="ObjectDetection_RT-DETR" \
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
    app.py
```

### Criar Bundle .app (Opcional)

Para criar um aplicativo macOS completo (.app):

```bash
# Após criar o executável, criar bundle
mkdir -p "ObjectDetection_RT-DETR.app/Contents/MacOS"
mkdir -p "ObjectDetection_RT-DETR.app/Contents/Resources"

# Copiar executável
cp dist/ObjectDetection_RT-DETR "ObjectDetection_RT-DETR.app/Contents/MacOS/"

# Criar Info.plist
cat > "ObjectDetection_RT-DETR.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ObjectDetection_RT-DETR</string>
    <key>CFBundleIdentifier</key>
    <string>com.realtec.objectdetection-rtdetr</string>
    <key>CFBundleName</key>
    <string>ObjectDetection RT-DETR</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
</dict>
</plist>
EOF
```

## 🪟 Criando Executável para Windows

### Método 1: Script Automatizado (Recomendado)

```cmd
REM Executar script
build_windows.bat
```

O script irá:
1. Criar ambiente virtual
2. Instalar dependências específicas do Windows
3. Criar executável usando PyInstaller
4. Gerar arquivo em `dist\ObjectDetection_RT-DETR.exe`

### Método 2: Manual

```cmd
REM 1. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate

REM 2. Instalar dependências
REM NOTA: Para GPU NVIDIA, instale PyTorch com CUDA primeiro:
REM pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements-windows.txt

REM 3. Instalar PyInstaller
pip install pyinstaller

REM 4. Criar executável
pyinstaller --name="ObjectDetection_RT-DETR" ^
    --onefile ^
    --windowed ^
    --add-data "config;config" ^
    --add-data "src;src" ^
    --add-data "data;data" ^
    --hidden-import="interface_tkinter" ^
    --hidden-import="src.train_rtdetr" ^
    --hidden-import="src.infer_images" ^
    --hidden-import="src.infer_video" ^
    --hidden-import="src.eval_coco" ^
    --hidden-import="src.hf_model_utils" ^
    --hidden-import="src.coco_utils" ^
    --hidden-import="src.utils.paths" ^
    --hidden-import="transformers.models.rtdetr" ^
    --hidden-import="torch" ^
    --hidden-import="cv2" ^
    --hidden-import="PIL" ^
    --hidden-import="pycocotools" ^
    --hidden-import="roboflow" ^
    --hidden-import="matplotlib.backends.backend_tkagg" ^
    --collect-all="torch" ^
    --collect-all="transformers" ^
    --collect-all="cv2" ^
    app.py
```

### Suporte CUDA no Windows

Para usar GPU NVIDIA no Windows:

1. Verificar versão CUDA instalada:
```cmd
nvcc --version
```

2. Instalar PyTorch com CUDA apropriado:
```cmd
REM Para CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM Para CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. Editar `requirements-windows.txt` e descomentar a linha apropriada

4. Reexecutar o build

## 🔧 Resolução de Problemas

### Problema: Executável muito grande

**Solução**: O executável inclui todas as dependências (PyTorch, Transformers, etc.) e pode ter 500MB-1GB. Isso é normal.

### Problema: Erro "ModuleNotFoundError"

**Solução**: Adicione o módulo faltante em `--hidden-import`:
```bash
pyinstaller ... --hidden-import="nome_do_modulo" ...
```

### Problema: Caminhos não funcionam no executável

**Solução**: O código já usa `Path(__file__)` que funciona em executáveis. Se houver problemas, verifique `src/utils/paths.py`.

### Problema: Executável não inicia no macOS

**Solução**: 
1. Verificar permissões: `chmod +x dist/ObjectDetection_RT-DETR`
2. Executar do terminal para ver erros: `./dist/ObjectDetection_RT-DETR`
3. Verificar se não há problemas de assinatura de código

### Problema: Executável não inicia no Windows

**Solução**:
1. Verificar se Visual C++ Redistributable está instalado
2. Executar do CMD para ver erros: `dist\ObjectDetection_RT-DETR.exe`
3. Verificar antivírus (pode bloquear executáveis PyInstaller)

## 📦 Distribuição

### macOS
- Distribua o arquivo `dist/ObjectDetection_RT-DETR` ou o bundle `.app`
- Usuários podem precisar permitir execução em "Preferências do Sistema > Segurança"

### Windows
- Distribua o arquivo `dist\ObjectDetection_RT-DETR.exe`
- Considere criar um instalador com [Inno Setup](https://jrsoftware.org/isinfo.php) ou [NSIS](https://nsis.sourceforge.io/)

## 📝 Notas Importantes

1. **Tamanho do Executável**: Pode ser grande (500MB-1GB) devido às dependências
2. **Primeira Execução**: Pode ser mais lenta enquanto extrai arquivos temporários
3. **Dependências Externas**: Modelos Hugging Face serão baixados na primeira execução
4. **Datasets**: Devem estar no diretório `data/datasets/` relativo ao executável
5. **Checkpoints**: Serão salvos em `data/models/experiments/` relativo ao executável

## 🚀 Testando o Executável

Após criar o executável:

1. **macOS**:
```bash
./dist/ObjectDetection_RT-DETR
```

2. **Windows**:
```cmd
dist\ObjectDetection_RT-DETR.exe
```

Verifique se:
- ✅ Interface abre corretamente
- ✅ Carregamento de datasets funciona
- ✅ Treinamento pode ser iniciado
- ✅ Predição funciona
- ✅ Checkpoints são salvos corretamente

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Execute com `--console` para ver mensagens de erro
3. Verifique se todas as dependências estão instaladas

