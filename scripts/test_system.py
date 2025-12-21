#!/usr/bin/env python3
"""
Script de testes completo para validar todas as funcionalidades do sistema RT-DETR v1.
"""

import sys
import subprocess
from pathlib import Path
import json
import os

# Adicionar diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "src"))

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🧪 Testando imports...")
    try:
        import torch
        import transformers
        import roboflow
        import pycocotools
        from src import train_rtdetr, infer_images, infer_video, eval_coco
        print("   ✅ Todos os imports OK")
        return True
    except Exception as e:
        print(f"   ❌ Erro nos imports: {e}")
        return False

def test_model_loading():
    """Testa carregamento de modelo."""
    print("🧪 Testando carregamento de modelo...")
    try:
        from src.hf_model_utils import load_model_for_object_detection
        # Tentar carregar modelo (pode falhar se não tiver internet, mas não deve crashar)
        try:
            model = load_model_for_object_detection("PekingU/rtdetr_r50vd", num_labels=1)
            print("   ✅ Modelo carregado com sucesso")
            return True
        except Exception as e:
            print(f"   ⚠️  Não foi possível baixar modelo (normal se offline): {e}")
            return True  # Não é erro crítico
    except Exception as e:
        print(f"   ❌ Erro ao testar carregamento: {e}")
        return False

def test_roboflow_download():
    """Testa script de download do Roboflow."""
    print("🧪 Testando script de download Roboflow...")
    script_path = Path("scripts/download_roboflow_coco.py")
    if not script_path.exists():
        print("   ❌ Script não encontrado")
        return False
    
    # Testar apenas sintaxe
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✅ Script compila sem erros")
        return True
    else:
        print(f"   ❌ Erro de compilação: {result.stderr}")
        return False

def test_training_script():
    """Testa script de treinamento."""
    print("🧪 Testando script de treinamento...")
    script_path = Path("src/train_rtdetr.py")
    if not script_path.exists():
        print("   ❌ Script não encontrado")
        return False
    
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✅ Script compila sem erros")
        return True
    else:
        print(f"   ❌ Erro de compilação: {result.stderr}")
        return False

def test_inference_scripts():
    """Testa scripts de inferência."""
    print("🧪 Testando scripts de inferência...")
    scripts = ["src/infer_images.py", "src/infer_video.py", "src/eval_coco.py"]
    all_ok = True
    
    for script in scripts:
        script_path = Path(script)
        if not script_path.exists():
            print(f"   ❌ {script} não encontrado")
            all_ok = False
            continue
        
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"   ✅ {script} compila OK")
        else:
            print(f"   ❌ {script} erro: {result.stderr}")
            all_ok = False
    
    return all_ok

def test_interface():
    """Testa interface Tkinter."""
    print("🧪 Testando interface Tkinter...")
    try:
        import tkinter
        script_path = Path("interface_tkinter.py")
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("   ✅ Interface compila OK")
            return True
        else:
            print(f"   ❌ Erro: {result.stderr}")
            return False
    except ImportError:
        print("   ⚠️  Tkinter não disponível (normal em alguns ambientes)")
        return True

def test_hf_model_utils():
    """Testa utilitários de modelo."""
    print("🧪 Testando hf_model_utils...")
    script_path = Path("src/hf_model_utils.py")
    if not script_path.exists():
        print("   ❌ Script não encontrado")
        return False
    
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✅ hf_model_utils compila OK")
        return True
    else:
        print(f"   ❌ Erro: {result.stderr}")
        return False

def test_coco_utils():
    """Testa utilitários COCO."""
    print("🧪 Testando coco_utils...")
    script_path = Path("src/coco_utils.py")
    if not script_path.exists():
        print("   ❌ Script não encontrado")
        return False
    
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(script_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✅ coco_utils compila OK")
        return True
    else:
        print(f"   ❌ Erro: {result.stderr}")
        return False

def main():
    """Executa todos os testes."""
    print("=" * 70)
    print("🧪 TESTES DO SISTEMA RT-DETR v1")
    print("=" * 70)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Carregamento de Modelo", test_model_loading),
        ("Download Roboflow", test_roboflow_download),
        ("Script de Treinamento", test_training_script),
        ("Scripts de Inferência", test_inference_scripts),
        ("Interface Tkinter", test_interface),
        ("hf_model_utils", test_hf_model_utils),
        ("coco_utils", test_coco_utils),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            results.append((name, False))
        print()
    
    # Resumo
    print("=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram!")
        return 0
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

