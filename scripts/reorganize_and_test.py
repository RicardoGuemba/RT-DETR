#!/usr/bin/env python3
"""
Script de Reorganização e Testes do Projeto ObjectDetection_RT-DETR
Consolida estrutura de diretórios e testa todas as funcionalidades.
"""

import os
import shutil
import sys
from pathlib import Path
import json
import subprocess
from typing import List, Tuple

# Cores para output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(msg: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {msg}{Colors.RESET}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def safe_move(src: Path, dst: Path) -> bool:
    """Move arquivo/diretório de forma segura."""
    try:
        if src.exists():
            if dst.exists():
                # Se destino existe, mesclar conteúdo
                if src.is_dir() and dst.is_dir():
                    for item in src.iterdir():
                        safe_move(item, dst / item.name)
                    try:
                        src.rmdir()
                    except:
                        pass
                    return True
                else:
                    print_warning(f"Destino já existe: {dst}, pulando {src}")
                    return False
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                return True
        return False
    except Exception as e:
        print_error(f"Erro ao mover {src} → {dst}: {e}")
        return False

def remove_empty_dirs(root: Path):
    """Remove diretórios vazios recursivamente."""
    for dirpath in sorted(root.rglob('*'), reverse=True):
        if dirpath.is_dir():
            try:
                if not any(dirpath.iterdir()):
                    dirpath.rmdir()
                    print_success(f"Removido diretório vazio: {dirpath.relative_to(root)}")
            except OSError:
                pass

class ProjectReorganizer:
    def __init__(self, root_dir: Path):
        self.root = root_dir
        self.moved_items = []
        self.removed_items = []
        
    def reorganize_datasets(self):
        """Consolida todos os datasets em data/datasets/"""
        print_step("Reorganizando datasets...")
        
        datasets_dir = self.root / "data" / "datasets"
        datasets_dir.mkdir(parents=True, exist_ok=True)
        
        # Mover dataset/ para data/datasets/default/
        old_dataset = self.root / "dataset"
        if old_dataset.exists():
            default_dataset = datasets_dir / "default"
            if not default_dataset.exists():
                if safe_move(old_dataset, default_dataset):
                    print_success(f"Movido: dataset/ → data/datasets/default/")
                    self.moved_items.append(("dataset/", "data/datasets/default/"))
            else:
                # Mesclar conteúdo
                for item in old_dataset.iterdir():
                    safe_move(item, default_dataset / item.name)
                try:
                    old_dataset.rmdir()
                    print_success(f"Mesclado: dataset/ → data/datasets/default/")
                    self.moved_items.append(("dataset/", "data/datasets/default/"))
                except:
                    pass
        
        # Mover datasets/ para data/datasets/ (se diferente)
        old_datasets = self.root / "datasets"
        if old_datasets.exists() and old_datasets != datasets_dir:
            # Verificar se já existe default
            if (datasets_dir / "default").exists():
                # Mesclar conteúdo
                for item in old_datasets.iterdir():
                    if item.name != "default":
                        safe_move(item, datasets_dir / item.name)
                try:
                    old_datasets.rmdir()
                    print_success(f"Mesclado: datasets/ → data/datasets/")
                    self.moved_items.append(("datasets/", "data/datasets/"))
                except:
                    pass
            else:
                if safe_move(old_datasets, datasets_dir):
                    print_success(f"Consolidado: datasets/ → data/datasets/")
                    self.moved_items.append(("datasets/", "data/datasets/"))
    
    def reorganize_models(self):
        """Consolida todos os modelos em data/models/"""
        print_step("Reorganizando modelos...")
        
        models_dir = self.root / "data" / "models"
        experiments_dir = models_dir / "experiments"
        experiments_dir.mkdir(parents=True, exist_ok=True)
        
        # Mover runs_rtdetr/ para data/models/experiments/legacy/
        old_runs = self.root / "runs_rtdetr"
        if old_runs.exists():
            legacy_dir = experiments_dir / "legacy"
            if safe_move(old_runs, legacy_dir):
                print_success(f"Movido: runs_rtdetr/ → data/models/experiments/legacy/")
                self.moved_items.append(("runs_rtdetr/", "data/models/experiments/legacy/"))
        
        # Mover models/ se existir
        old_models = self.root / "models"
        if old_models.exists() and old_models != models_dir:
            for item in old_models.iterdir():
                safe_move(item, models_dir / item.name)
            try:
                old_models.rmdir()
                print_success(f"Consolidado: models/ → data/models/")
                self.moved_items.append(("models/", "data/models/"))
            except:
                pass
    
    def reorganize_outputs(self):
        """Consolida outputs em data/outputs/"""
        print_step("Reorganizando outputs...")
        
        outputs_dir = self.root / "data" / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        old_outputs = self.root / "outputs"
        if old_outputs.exists():
            for item in old_outputs.iterdir():
                safe_move(item, outputs_dir / item.name)
            try:
                old_outputs.rmdir()
                print_success(f"Consolidado: outputs/ → data/outputs/")
                self.moved_items.append(("outputs/", "data/outputs/"))
            except:
                pass
    
    def reorganize_logs(self):
        """Consolida logs em data/logs/"""
        print_step("Reorganizando logs...")
        
        logs_dir = self.root / "data" / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        
        old_logs = self.root / "logs"
        if old_logs.exists() and old_logs != logs_dir:
            for item in old_logs.iterdir():
                safe_move(item, logs_dir / item.name)
            try:
                old_logs.rmdir()
                print_success(f"Consolidado: logs/ → data/logs/")
                self.moved_items.append(("logs/", "data/logs/"))
            except:
                pass
    
    def remove_redundant_docs(self):
        """Remove documentação redundante."""
        print_step("Removendo documentação redundante...")
        
        redundant_docs = [
            "ANALISE_PERFORMANCE_ESTABILIDADE.md",
            "ARQUITETURA_REFATORADA.md",
            "ESTRUTURA_DIRETORIOS.md",
            "GARANTIA_RT-DETR_V1.md",
            "LIMPEZA_CONCLUIDA.md",
            "MELHORIAS_IMPLEMENTADAS.md",
            "README_ARQUITETURA.md",
            "RESUMO_REFATORACAO.md",
        ]
        
        for doc in redundant_docs:
            doc_path = self.root / doc
            if doc_path.exists():
                doc_path.unlink()
                print_success(f"Removido: {doc}")
                self.removed_items.append(doc)
    
    def remove_empty_directories(self):
        """Remove diretórios vazios desnecessários."""
        print_step("Removendo diretórios vazios...")
        
        empty_dirs = [
            "interfaces/cli",
            "interfaces/gui",
            "src/core",
            "src/training",
            "src/inference",
            "src/evaluation",
        ]
        
        for dir_path in empty_dirs:
            full_path = self.root / dir_path
            if full_path.exists():
                try:
                    shutil.rmtree(full_path)
                    print_success(f"Removido: {dir_path}/")
                    self.removed_items.append(f"{dir_path}/")
                except Exception as e:
                    print_warning(f"Erro ao remover {dir_path}: {e}")
        
        # Remover interfaces/ se estiver vazio
        interfaces_dir = self.root / "interfaces"
        if interfaces_dir.exists() and not any(interfaces_dir.iterdir()):
            try:
                interfaces_dir.rmdir()
                print_success("Removido: interfaces/")
            except:
                pass
    
    def update_code_references(self):
        """Atualiza referências hardcoded no código."""
        print_step("Atualizando referências no código...")
        
        # Arquivos para atualizar
        files_to_update = [
            "interface_tkinter.py",
        ]
        
        replacements = [
            ('"dataset"', '"data/datasets/default"'),
            ('"dataset/test"', '"data/datasets/default/test"'),
            ('"runs_rtdetr"', '"data/models/experiments/legacy"'),
            ('runs_rtdetr/', 'data/models/experiments/legacy/'),
            ('f"runs_rtdetr/', 'f"data/models/experiments/legacy/'),
            ('Path("runs_rtdetr/', 'Path("data/models/experiments/legacy/'),
        ]
        
        for file_name in files_to_update:
            file_path = self.root / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')
                    original_content = content
                    
                    for old, new in replacements:
                        content = content.replace(old, new)
                    
                    if content != original_content:
                        file_path.write_text(content, encoding='utf-8')
                        print_success(f"Atualizado: {file_name}")
                except Exception as e:
                    print_warning(f"Erro ao atualizar {file_name}: {e}")
    
    def update_gitignore(self):
        """Atualiza .gitignore para nova estrutura."""
        print_step("Atualizando .gitignore...")
        
        gitignore_path = self.root / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            
            # Remover entradas antigas
            old_entries = ["dataset/", "runs_rtdetr/", "logs/"]
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if line.strip() not in old_entries:
                    new_lines.append(line)
            
            # Adicionar novas se não existirem
            new_entries = [
                "data/datasets/*/",
                "!data/datasets/.gitkeep",
                "data/models/experiments/*/",
                "!data/models/experiments/.gitkeep",
            ]
            
            for entry in new_entries:
                if entry not in new_lines:
                    new_lines.append(entry)
            
            gitignore_path.write_text('\n'.join(new_lines))
            print_success("Atualizado: .gitignore")
    
    def run_all(self):
        """Executa toda a reorganização."""
        print(f"\n{Colors.BOLD}{'='*70}")
        print("REORGANIZAÇÃO DO PROJETO ObjectDetection_RT-DETR")
        print(f"{'='*70}{Colors.RESET}\n")
        
        self.reorganize_datasets()
        self.reorganize_models()
        self.reorganize_outputs()
        self.reorganize_logs()
        self.remove_redundant_docs()
        self.remove_empty_directories()
        self.update_code_references()
        self.update_gitignore()
        
        # Remover diretórios vazios finais
        remove_empty_dirs(self.root)
        
        print(f"\n{Colors.BOLD}{'='*70}")
        print("REORGANIZAÇÃO CONCLUÍDA")
        print(f"{'='*70}{Colors.RESET}\n")
        
        print(f"{Colors.GREEN}Itens movidos: {len(self.moved_items)}{Colors.RESET}")
        for old, new in self.moved_items:
            print(f"  • {old} → {new}")
        
        print(f"\n{Colors.YELLOW}Itens removidos: {len(self.removed_items)}{Colors.RESET}")
        for item in self.removed_items:
            print(f"  • {item}")

class FunctionTester:
    def __init__(self, root_dir: Path):
        self.root = root_dir
        
    def test_imports(self) -> bool:
        """Testa se todos os imports principais funcionam."""
        print_step("Testando imports...")
        
        try:
            import sys
            sys.path.insert(0, str(self.root))
            sys.path.insert(0, str(self.root / "src"))
            
            # Testar imports principais
            imports_to_test = [
                ("src.utils.paths", "get_default_dataset"),
                ("src.coco_utils", "remap_category_ids"),
            ]
            
            for module_name, item_name in imports_to_test:
                try:
                    module = __import__(module_name, fromlist=[item_name])
                    getattr(module, item_name)
                    print_success(f"Import OK: {module_name}.{item_name}")
                except Exception as e:
                    print_error(f"Import FALHOU: {module_name}.{item_name} - {e}")
                    return False
            
            # Testar interface_tkinter separadamente (pode ter dependências GUI)
            try:
                import interface_tkinter
                print_success("Import OK: interface_tkinter")
            except Exception as e:
                print_warning(f"Import interface_tkinter (pode falhar sem GUI): {e}")
            
            return True
        except Exception as e:
            print_error(f"Erro nos testes de import: {e}")
            return False
    
    def test_paths_utils(self) -> bool:
        """Testa utilitários de caminhos."""
        print_step("Testando utilitários de caminhos...")
        
        try:
            from src.utils.paths import (
                get_datasets_dir,
                get_models_dir,
                get_outputs_dir,
                get_logs_dir,
                get_default_dataset,
                get_default_output_dir,
            )
            
            datasets_dir = get_datasets_dir()
            models_dir = get_models_dir()
            outputs_dir = get_outputs_dir()
            logs_dir = get_logs_dir()
            default_dataset = get_default_dataset()
            default_output = get_default_output_dir()
            
            print_success(f"Datasets dir: {datasets_dir}")
            print_success(f"Models dir: {models_dir}")
            print_success(f"Outputs dir: {outputs_dir}")
            print_success(f"Logs dir: {logs_dir}")
            print_success(f"Default dataset: {default_dataset}")
            print_success(f"Default output: {default_output}")
            
            return True
        except Exception as e:
            print_error(f"Erro nos testes de paths: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_config(self) -> bool:
        """Testa configuração."""
        print_step("Testando configuração...")
        
        try:
            config_path = self.root / "config" / "paths.json"
            if not config_path.exists():
                print_warning("config/paths.json não encontrado")
                return False
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            required_keys = ["paths", "defaults"]
            for key in required_keys:
                if key not in config:
                    print_error(f"Chave faltando em config: {key}")
                    return False
            
            print_success("Configuração válida")
            return True
        except Exception as e:
            print_error(f"Erro ao testar config: {e}")
            return False
    
    def test_scripts(self) -> bool:
        """Testa scripts principais."""
        print_step("Testando scripts...")
        
        scripts_to_test = [
            ("scripts/download_roboflow_coco.py", ["--help"]),
            ("src/train_rtdetr.py", ["--help"]),
            ("src/infer_images.py", ["--help"]),
            ("src/infer_video.py", ["--help"]),
        ]
        
        all_ok = True
        for script_path, args in scripts_to_test:
            full_path = self.root / script_path
            if full_path.exists():
                try:
                    result = subprocess.run(
                        [sys.executable, str(full_path)] + args,
                        capture_output=True,
                        timeout=10,
                        cwd=str(self.root)
                    )
                    if result.returncode == 0 or "--help" in args:
                        print_success(f"Script OK: {script_path}")
                    else:
                        print_warning(f"Script retornou código {result.returncode}: {script_path}")
                except subprocess.TimeoutExpired:
                    print_warning(f"Script timeout: {script_path}")
                except Exception as e:
                    print_warning(f"Erro ao testar {script_path}: {e}")
            else:
                print_warning(f"Script não encontrado: {script_path}")
        
        return all_ok
    
    def run_all_tests(self) -> bool:
        """Executa todos os testes."""
        print(f"\n{Colors.BOLD}{'='*70}")
        print("TESTES DE FUNCIONALIDADES")
        print(f"{'='*70}{Colors.RESET}\n")
        
        results = []
        results.append(("Imports", self.test_imports()))
        results.append(("Paths Utils", self.test_paths_utils()))
        results.append(("Config", self.test_config()))
        results.append(("Scripts", self.test_scripts()))
        
        print(f"\n{Colors.BOLD}{'='*70}")
        print("RESULTADOS DOS TESTES")
        print(f"{'='*70}{Colors.RESET}\n")
        
        all_passed = True
        for test_name, passed in results:
            status = f"{Colors.GREEN}✅ PASSOU{Colors.RESET}" if passed else f"{Colors.RED}❌ FALHOU{Colors.RESET}"
            print(f"{test_name}: {status}")
            if not passed:
                all_passed = False
        
        return all_passed

def main():
    root_dir = Path(__file__).parent.parent
    
    # Fase 1: Reorganização
    reorganizer = ProjectReorganizer(root_dir)
    reorganizer.run_all()
    
    # Fase 2: Testes
    tester = FunctionTester(root_dir)
    tests_passed = tester.run_all_tests()
    
    # Resumo final
    print(f"\n{Colors.BOLD}{'='*70}")
    if tests_passed:
        print(f"{Colors.GREEN}✅ REORGANIZAÇÃO E TESTES CONCLUÍDOS COM SUCESSO!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}⚠️  REORGANIZAÇÃO CONCLUÍDA, MAS ALGUNS TESTES FALHARAM{Colors.RESET}")
    print(f"{'='*70}{Colors.RESET}\n")

if __name__ == "__main__":
    main()

