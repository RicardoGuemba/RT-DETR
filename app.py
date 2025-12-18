#!/usr/bin/env python3
"""
Aplicação principal ObjectDetection_RT-DETR - Sistema de Detecção de Objetos
Ponto de entrada principal do sistema.
"""

import sys
import os
from pathlib import Path

# Adicionar diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_dependencies():
    """Verifica se as dependências principais estão instaladas."""
    missing = []
    
    try:
        import torch
    except ImportError:
        missing.append("torch")
    
    try:
        import transformers
    except ImportError:
        missing.append("transformers")
    
    try:
        import roboflow
    except ImportError:
        missing.append("roboflow")
    
    try:
        import pycocotools
    except ImportError:
        missing.append("pycocotools")
    
    return missing

def main():
    """Função principal que inicia a interface."""
    print("🚀 ObjectDetection_RT-DETR - Sistema de Detecção de Objetos")
    print("=" * 60)
    print()
    
    # Verificar se estamos no ambiente virtual (venv ou conda)
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    in_conda = 'CONDA_DEFAULT_ENV' in os.environ or 'CONDA_PREFIX' in os.environ
    
    if not in_venv and not in_conda:
        print("⚠️  AVISO: Ambiente virtual não detectado!")
        print("   Recomendado:")
        print("   - Para venv: source .venv/bin/activate")
        print("   - Para conda: conda activate seu_ambiente")
        print()
        resposta = input("Continuar mesmo assim? (s/N): ").strip().lower()
        if resposta != 's':
            print("Operação cancelada.")
            sys.exit(0)
        print()
    else:
        env_type = "conda" if in_conda else "venv"
        env_name = os.environ.get('CONDA_DEFAULT_ENV', 'venv')
        print(f"✅ Ambiente {env_type} detectado: {env_name}")
        print()
    
    # Verificar dependências
    missing_deps = check_dependencies()
    if missing_deps:
        print("⚠️  AVISO: Algumas dependências não estão instaladas:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print()
        print("Opções:")
        print("   1. Instalar dependências agora (recomendado)")
        print("   2. Continuar mesmo assim (algumas funcionalidades podem não funcionar)")
        print("   3. Cancelar e instalar manualmente")
        print()
        resposta = input("Escolha uma opção [1]: ").strip().lower()
        
        if resposta == "" or resposta == "1":
            # Tentar instalar automaticamente
            print()
            print("📦 Instalando dependências...")
            try:
                import subprocess
                cmd = [sys.executable, "-m", "pip", "install"] + missing_deps
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                print("✅ Dependências instaladas com sucesso!")
                print()
                # Verificar novamente
                missing_deps = check_dependencies()
                if missing_deps:
                    print(f"⚠️  Ainda faltam: {', '.join(missing_deps)}")
                    print("   Tente instalar manualmente: pip install -r requirements.txt")
                    print()
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar dependências: {e}")
                print()
                print("💡 Instale manualmente executando:")
                print(f"   pip install {' '.join(missing_deps)}")
                print("   ou")
                print("   pip install -r requirements.txt")
                print()
                resposta2 = input("Continuar mesmo assim? (s/N): ").strip().lower()
                if resposta2 != 's':
                    print("Operação cancelada.")
                    sys.exit(0)
            except Exception as e:
                print(f"❌ Erro: {e}")
                print("   Instale manualmente: pip install -r requirements.txt")
                resposta2 = input("Continuar mesmo assim? (s/N): ").strip().lower()
                if resposta2 != 's':
                    print("Operação cancelada.")
                    sys.exit(0)
        elif resposta == "2":
            print()
            print("⚠️  Continuando sem algumas dependências. Algumas funcionalidades podem não funcionar.")
            print()
        else:
            print()
            print("💡 Para instalar as dependências manualmente, execute:")
            print(f"   pip install {' '.join(missing_deps)}")
            print("   ou")
            print("   pip install -r requirements.txt")
            print()
            print("Operação cancelada.")
            sys.exit(0)
    
    # Iniciar diretamente a interface gráfica Tkinter (totalmente gráfica)
    print("🖥️  Iniciando Interface Gráfica Tkinter...")
    print("   (Interface totalmente gráfica - sem necessidade de linha de comando)")
    print()
    
    try:
        import tkinter as tk
        import interface_tkinter
        print("✅ Interface carregada com sucesso!")
        print("   A janela será aberta em instantes...")
        print()
        root = tk.Tk()
        app = interface_tkinter.ModernTkinterApp(root)
        root.mainloop()
        print("\n👋 Interface Tkinter encerrada.")
    except ImportError as e:
        print(f"❌ Erro ao importar interface Tkinter: {e}")
        print("   Certifique-se de que tkinter está instalado.")
        print()
        print("💡 Alternativa: Use a interface CLI")
        print("   python interface.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()




