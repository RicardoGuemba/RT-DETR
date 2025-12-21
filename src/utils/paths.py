"""
Utilitários para gerenciamento de caminhos do sistema.
Centraliza todos os caminhos padrão para facilitar manutenção.
"""

from pathlib import Path
import json
import sys
from typing import Optional

# Detectar se estamos rodando como executável PyInstaller
if getattr(sys, 'frozen', False):
    # Executável PyInstaller: tentar encontrar diretório raiz do projeto
    # O executável está em Contents/Resources/, então precisamos subir até o diretório raiz
    exe_path = Path(sys.executable)
    # Se estamos em um .app bundle, subir até encontrar o diretório raiz
    # Caso contrário, usar o diretório do executável
    if exe_path.parent.name == "Resources" and exe_path.parent.parent.name == "Contents":
        # Estamos em um .app bundle, tentar encontrar diretório raiz
        # O diretório raiz deve estar ao lado do .app ou dentro dele
        app_dir = exe_path.parent.parent.parent  # Contents/Resources -> Contents -> .app
        # Tentar encontrar dataset ou outros arquivos do projeto
        if (app_dir / "dataset").exists() or (app_dir / "runs_rtdetr").exists():
            ROOT_DIR = app_dir
        else:
            # Tentar diretório pai do .app
            parent_dir = app_dir.parent
            if (parent_dir / "dataset").exists() or (parent_dir / "runs_rtdetr").exists():
                ROOT_DIR = parent_dir
            else:
                # Fallback: usar diretório do executável
                ROOT_DIR = exe_path.parent
    else:
        # Executável standalone, usar diretório do executável
        ROOT_DIR = exe_path.parent
else:
    # Script Python normal: usar diretório do script (comportamento original)
    ROOT_DIR = Path(__file__).parent.parent.parent

# Tentar carregar configuração de caminhos
PATHS_CONFIG = None
try:
    config_file = ROOT_DIR / "config" / "paths.json"
    if config_file.exists():
        with open(config_file, 'r') as f:
            PATHS_CONFIG = json.load(f)
except Exception:
    pass

def get_datasets_dir() -> Path:
    """Retorna diretório de datasets."""
    if PATHS_CONFIG:
        return ROOT_DIR / PATHS_CONFIG["paths"]["datasets"]
    # Fallback para estrutura antiga
    return ROOT_DIR / "data" / "datasets" if (ROOT_DIR / "data" / "datasets").exists() else ROOT_DIR / "dataset"

def get_models_dir() -> Path:
    """Retorna diretório de modelos."""
    if PATHS_CONFIG:
        return ROOT_DIR / PATHS_CONFIG["paths"]["models"]
    # Fallback para estrutura antiga
    return ROOT_DIR / "data" / "models" / "experiments" if (ROOT_DIR / "data" / "models" / "experiments").exists() else ROOT_DIR / "runs_rtdetr"

def get_outputs_dir() -> Path:
    """Retorna diretório de outputs."""
    if PATHS_CONFIG:
        return ROOT_DIR / PATHS_CONFIG["paths"]["outputs"]
    # Fallback para estrutura antiga
    return ROOT_DIR / "data" / "outputs" / "predictions" if (ROOT_DIR / "data" / "outputs" / "predictions").exists() else ROOT_DIR / "outputs"

def get_logs_dir() -> Path:
    """Retorna diretório de logs."""
    if PATHS_CONFIG:
        return ROOT_DIR / PATHS_CONFIG["paths"]["logs"]
    # Fallback para estrutura antiga
    return ROOT_DIR / "data" / "logs" / "training" if (ROOT_DIR / "data" / "logs" / "training").exists() else ROOT_DIR / "logs"

def get_default_dataset() -> Path:
    """Retorna dataset padrão."""
    if PATHS_CONFIG:
        default_path = ROOT_DIR / PATHS_CONFIG["defaults"]["dataset"]
        if default_path.exists():
            return default_path
    
    # Fallback: tentar vários locais
    possible_paths = [
        ROOT_DIR / "data" / "datasets" / "default",
        ROOT_DIR / "dataset",
        ROOT_DIR / "datasets" / "default",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # Retornar primeiro existente ou criar padrão
    datasets_dir = get_datasets_dir()
    default = datasets_dir / "default"
    default.mkdir(parents=True, exist_ok=True)
    return default

def get_default_output_dir() -> Path:
    """Retorna diretório de output padrão."""
    if PATHS_CONFIG:
        default_path = ROOT_DIR / PATHS_CONFIG["defaults"]["output"]
        default_path.mkdir(parents=True, exist_ok=True)
        return default_path
    
    # Fallback
    models_dir = get_models_dir()
    default = models_dir / "default"
    default.mkdir(parents=True, exist_ok=True)
    return default

def resolve_path(path: str | Path, base: Optional[Path] = None) -> Path:
    """Resolve um caminho relativo ou absoluto."""
    path_obj = Path(path)
    
    if path_obj.is_absolute():
        return path_obj
    
    if base:
        return (base / path_obj).resolve()
    
    return (ROOT_DIR / path_obj).resolve()

