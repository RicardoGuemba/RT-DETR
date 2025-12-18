#!/usr/bin/env python3
"""
Script de teste rápido para verificar se o ambiente está configurado corretamente.
"""

import sys
from pathlib import Path

def test_imports():
    """Testa se todas as dependências principais estão instaladas."""
    print("🔍 Testando imports...")
    errors = []
    
    try:
        import torch
        print(f"  ✅ PyTorch {torch.__version__}")
        if torch.backends.mps.is_available():
            print("  ✅ MPS disponível")
        else:
            print("  ⚠️  MPS não disponível (usando CPU)")
    except ImportError as e:
        errors.append(f"PyTorch: {e}")
        print(f"  ❌ PyTorch não encontrado")
    
    try:
        import transformers
        print(f"  ✅ Transformers {transformers.__version__}")
    except ImportError as e:
        errors.append(f"Transformers: {e}")
        print(f"  ❌ Transformers não encontrado")
    
    try:
        import roboflow
        print(f"  ✅ Roboflow")
    except ImportError as e:
        errors.append(f"Roboflow: {e}")
        print(f"  ⚠️  Roboflow não encontrado (opcional)")
    
    try:
        import pycocotools
        print(f"  ✅ pycocotools")
    except ImportError as e:
        errors.append(f"pycocotools: {e}")
        print(f"  ❌ pycocotools não encontrado")
    
    try:
        import cv2
        print(f"  ✅ OpenCV {cv2.__version__}")
    except ImportError as e:
        errors.append(f"OpenCV: {e}")
        print(f"  ⚠️  OpenCV não encontrado (necessário para vídeo)")
    
    return len(errors) == 0

def test_structure():
    """Testa se a estrutura de diretórios está correta."""
    print("\n📁 Testando estrutura de diretórios...")
    
    required_dirs = [
        "src",
        "scripts",
        "docs",
        "data/downloads",
        "data/videos",
        "outputs/models",
        "outputs/inference",
        "outputs/logs"
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ⚠️  {dir_path}/ (será criado quando necessário)")
    
    return all_ok

def test_files():
    """Testa se os arquivos principais existem."""
    print("\n📄 Testando arquivos principais...")
    
    required_files = [
        "app.py",
        "interface_tkinter.py",
        "src/train_rtdetr.py",
        "src/infer_images.py",
        "src/infer_video.py",
        "requirements.txt"
    ]
    
    all_ok = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} não encontrado")
            all_ok = False
    
    return all_ok

def test_threshold_defaults():
    """Testa se os thresholds padrão estão configurados como 0.8."""
    print("\n🎯 Testando thresholds padrão...")
    
    try:
        # Testar infer_images.py
        with open("src/infer_images.py", "r") as f:
            content = f.read()
            if 'score_threshold: float = 0.8' in content or 'default=0.8' in content:
                print("  ✅ infer_images.py: threshold padrão = 0.8")
            else:
                print("  ⚠️  infer_images.py: threshold padrão pode não estar em 0.8")
        
        # Testar infer_video.py
        with open("src/infer_video.py", "r") as f:
            content = f.read()
            if 'score_threshold: float = 0.8' in content or 'default=0.8' in content:
                print("  ✅ infer_video.py: threshold padrão = 0.8")
            else:
                print("  ⚠️  infer_video.py: threshold padrão pode não estar em 0.8")
        
        # Testar interface_tkinter.py
        with open("interface_tkinter.py", "r") as f:
            content = f.read()
            if 'value=0.8' in content or 'value="0.8"' in content:
                print("  ✅ interface_tkinter.py: threshold padrão = 0.8")
            else:
                print("  ⚠️  interface_tkinter.py: threshold padrão pode não estar em 0.8")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao testar thresholds: {e}")
        return False

def main():
    """Executa todos os testes."""
    print("="*70)
    print("🧪 TESTE DE CONFIGURAÇÃO DO AMBIENTE")
    print("="*70)
    print()
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Estrutura", test_structure()))
    results.append(("Arquivos", test_files()))
    results.append(("Thresholds", test_threshold_defaults()))
    
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASSOU" if passed else "⚠️  AVISOS"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n✅ Todos os testes passaram! Ambiente configurado corretamente.")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os avisos acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

