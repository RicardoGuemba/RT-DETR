#!/usr/bin/env python3
"""
Script de migração para nova arquitetura refatorada.
Cria nova estrutura de diretórios e atualiza referências.
"""

import os
import shutil
from pathlib import Path
import json

def create_new_structure(root_dir: Path):
    """Cria nova estrutura de diretórios."""
    print("📁 Criando nova estrutura de diretórios...")
    
    directories = [
        # Data
        root_dir / "data" / "datasets" / "default",
        root_dir / "data" / "models" / "experiments",
        root_dir / "data" / "models" / "pretrained",
        root_dir / "data" / "outputs" / "predictions",
        root_dir / "data" / "outputs" / "evaluations",
        root_dir / "data" / "logs" / "training",
        root_dir / "data" / "logs" / "tensorboard",
        
        # Source (reorganizado)
        root_dir / "src" / "core",
        root_dir / "src" / "training",
        root_dir / "src" / "inference",
        root_dir / "src" / "evaluation",
        root_dir / "src" / "utils",
        
        # Scripts (reorganizado)
        root_dir / "scripts" / "setup",
        root_dir / "scripts" / "data",
        root_dir / "scripts" / "utils",
        
        # Outros
        root_dir / "config",
        root_dir / "tests" / "unit",
        root_dir / "tests" / "integration",
        root_dir / "tests" / "fixtures",
        root_dir / "docs" / "api",
        root_dir / "docs" / "guides",
        root_dir / "docs" / "architecture",
        root_dir / "interfaces" / "gui",
        root_dir / "interfaces" / "cli",
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_path.relative_to(root_dir)}")
    
    print("✅ Estrutura criada com sucesso!\n")

def migrate_files(root_dir: Path):
    """Migra arquivos para nova estrutura."""
    print("📦 Migrando arquivos...")
    
    migrations = [
        # Datasets
        (root_dir / "dataset", root_dir / "data" / "datasets" / "default", "dataset"),
        (root_dir / "datasets", root_dir / "data" / "datasets", "datasets"),
        
        # Models
        (root_dir / "runs_rtdetr", root_dir / "data" / "models" / "experiments" / "default", "runs_rtdetr"),
        (root_dir / "models", root_dir / "data" / "models" / "pretrained", "models"),
        
        # Outputs
        (root_dir / "outputs", root_dir / "data" / "outputs" / "predictions", "outputs"),
        
        # Logs
        (root_dir / "logs", root_dir / "data" / "logs" / "training", "logs"),
    ]
    
    for source, dest, name in migrations:
        if source.exists() and source.is_dir():
            if not dest.exists() or not any(dest.iterdir()):
                print(f"   📦 Migrando {name}...")
                try:
                    # Se destino já existe e tem conteúdo, não sobrescrever
                    if dest.exists() and any(dest.iterdir()):
                        print(f"      ⚠️  {dest} já existe com conteúdo, pulando...")
                    else:
                        if dest.exists():
                            dest.rmdir()
                        shutil.copytree(source, dest)
                        print(f"      ✅ {name} migrado para {dest.relative_to(root_dir)}")
                except Exception as e:
                    print(f"      ⚠️  Erro ao migrar {name}: {e}")
            else:
                print(f"   ⏭️  {name} já migrado")
        else:
            print(f"   ⏭️  {name} não existe, pulando")
    
    print("✅ Migração de arquivos concluída!\n")

def create_path_config(root_dir: Path):
    """Cria arquivo de configuração de caminhos."""
    print("⚙️  Criando configuração de caminhos...")
    
    config = {
        "paths": {
            "datasets": "data/datasets",
            "models": "data/models/experiments",
            "pretrained_models": "data/models/pretrained",
            "outputs": "data/outputs/predictions",
            "evaluations": "data/outputs/evaluations",
            "logs": "data/logs/training",
            "tensorboard_logs": "data/logs/tensorboard",
        },
        "defaults": {
            "dataset": "data/datasets/default",
            "output": "data/models/experiments/default",
            "model": "data/models/experiments/default/model_best",
        }
    }
    
    config_file = root_dir / "config" / "paths.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"   ✅ Configuração salva em {config_file.relative_to(root_dir)}\n")

def main():
    """Executa migração."""
    root_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("🏗️  MIGRAÇÃO PARA NOVA ARQUITETURA")
    print("=" * 70)
    print()
    
    print(f"📂 Diretório raiz: {root_dir}")
    print()
    
    # Confirmar
    resposta = input("Deseja continuar com a migração? (s/N): ").strip().lower()
    if resposta != 's':
        print("Migração cancelada.")
        return
    
    print()
    
    # Criar estrutura
    create_new_structure(root_dir)
    
    # Migrar arquivos
    migrate_files(root_dir)
    
    # Criar configuração
    create_path_config(root_dir)
    
    print("=" * 70)
    print("✅ MIGRAÇÃO CONCLUÍDA!")
    print("=" * 70)
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("1. Revisar arquivos migrados")
    print("2. Atualizar código para usar novos caminhos")
    print("3. Testar funcionalidades")
    print("4. Remover estrutura antiga (após validação)")
    print()

if __name__ == "__main__":
    main()

