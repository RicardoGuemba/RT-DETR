@echo off
REM Script para criar executável Windows do ObjectDetection_RT-DETR

echo ====================================
echo Criando executavel para Windows...
echo ====================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python nao encontrado
    echo Instale Python 3.8 ou superior de https://www.python.org/
    pause
    exit /b 1
)

echo Python encontrado
python --version
echo.

REM Criar ambiente virtual se nao existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip setuptools wheel

REM Instalar dependencias especificas do Windows
echo Instalando dependencias para Windows...
echo.
echo NOTA: Para GPU NVIDIA com CUDA, descomente as linhas apropriadas em requirements-windows.txt
echo       e instale PyTorch com suporte CUDA manualmente antes de continuar.
echo.
pause

pip install -r requirements-windows.txt

REM Verificar PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpar builds anteriores
echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM Criar executavel
echo Criando executavel...
pyinstaller ^
    --name="ObjectDetection_RT-DETR" ^
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
    --exclude-module="matplotlib.tests" ^
    --exclude-module="numpy.tests" ^
    --exclude-module="scipy.tests" ^
    --exclude-module="torch.test" ^
    app.py

REM Verificar se o executavel foi criado
if exist "dist\ObjectDetection_RT-DETR.exe" (
    echo.
    echo ====================================
    echo Executavel criado com sucesso!
    echo ====================================
    echo Localizacao: dist\ObjectDetection_RT-DETR.exe
    echo.
    echo Proximos passos:
    echo    1. Teste o executavel: dist\ObjectDetection_RT-DETR.exe
    echo    2. Se funcionar, voce pode distribuir o arquivo
    echo    3. Considere criar um instalador com Inno Setup ou NSIS
    echo.
) else (
    echo Erro: Executavel nao foi criado
    pause
    exit /b 1
)

pause

