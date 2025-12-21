"""
Utilitários para resolver caminhos quando executando como executável PyInstaller.
"""

import sys
from pathlib import Path
import os


def get_base_dir() -> Path:
    """
    Retorna o diretório base do aplicativo.
    Se executando como PyInstaller, retorna o diretório do executável.
    Caso contrário, retorna o diretório do script.
    """
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        # sys._MEIPASS é o diretório temporário onde PyInstaller extrai arquivos
        # sys.executable é o caminho do executável
        return Path(sys.executable).parent
    else:
        # Script Python normal
        return Path(__file__).parent.parent.parent


def get_resource_path(relative_path: str) -> Path:
    """
    Retorna o caminho absoluto para um recurso.
    Funciona tanto em modo desenvolvimento quanto em executável.
    """
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        # Tentar primeiro no diretório do executável
        exe_dir = Path(sys.executable).parent
        resource_path = exe_dir / relative_path
        if resource_path.exists():
            return resource_path
        
        # Se não encontrado, tentar no diretório temporário (sys._MEIPASS)
        base_path = Path(sys._MEIPASS)
        return base_path / relative_path
    else:
        # Script Python normal
        base_path = Path(__file__).parent.parent.parent
        return base_path / relative_path


def ensure_data_dirs():
    """
    Garante que os diretórios de dados existam no diretório do executável.
    """
    base_dir = get_base_dir()
    
    # Criar estrutura de diretórios necessária
    dirs_to_create = [
        "data/datasets/default",
        "data/models/experiments/default",
        "data/outputs/predictions",
        "data/logs/training",
        "config"
    ]
    
    for dir_path in dirs_to_create:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
    
    return base_dir

